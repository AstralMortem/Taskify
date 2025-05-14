from datetime import UTC, datetime, timedelta
import hashlib
from typing import Any
import uuid
from fastapi import Response
import jwt
from taskify.config import settings
from taskify.core.exception import TaskifyException, status
from taskify.models.auth import User
from taskify.repositories.auth import UserRepository
from taskify.repositories.oauth import OAuthRepository
from taskify.schemas.auth import LoginCredentials, ResetPasswordCredentials
from taskify.schemas.user import UserCreate
from taskify.utils.password_helper import PasswordHelperProtocol, PasswordHelper
from httpx_oauth.oauth2 import OAuth2Token, BaseOAuth2


class AuthService:
    def __init__(
        self,
        repository: UserRepository,
        oauth_repository: OAuthRepository,
        password_helper: PasswordHelperProtocol = PasswordHelper(),
    ):
        self.repo = repository
        self.oauth_repo = oauth_repository
        self.password_helper = password_helper

    async def login(self, credentials: LoginCredentials):
        error = TaskifyException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid credentials",
            "Invalid Email/Password",
        )
        exist = await self.repo.get_by_email(credentials.email)
        if exist is None:
            exist = await self.repo.get_by_username(credentials.email)
            if exist is None:
                raise error

        is_valid_password, new_hash = self.password_helper.verify_and_update(
            credentials.password, exist.hashed_password
        )
        if not is_valid_password:
            raise error

        if new_hash:
            exist = await self.repo.update(exist, {"hashed_password": new_hash})

        if not exist.is_active:
            raise error

        return self._create_login_response(exist)

    async def signup(self, payload: UserCreate, safe: bool = True) -> User:
        for key in ["email", "username"]:
            if value := getattr(payload, key, None):
                if await self.repo.get_by_field(key, value) is not None:
                    raise TaskifyException(
                        status.HTTP_400_BAD_REQUEST,
                        "User already exist",
                        f"User with provided {key} {value} already exist",
                    )

        dump_payload = payload.model_dump()
        dump_payload["hashed_password"] = self.password_helper.hash(
            dump_payload.pop("password")
        )
        # If user not set username, generate hash from email, and slice it
        if not dump_payload.get("username", False):
            dump_payload["username"] = hashlib.sha256(
                payload.email.encode()
            ).hexdigest()[:20]

        if safe:
            dump_payload["role_id"] = settings.DEFAULT_ROLE_ID
            dump_payload["is_active"] = True

        return await self.repo.create(dump_payload)

    async def authenticate(self, token: str):
        payload = self._decode_jwt_token(token, settings.JWT_AUTH_TOKEN_AUDIENCE)
        try:
            user_id = uuid.UUID(payload.get("sub"))
        except Exception as e:
            raise TaskifyException(
                status.HTTP_401_UNAUTHORIZED, "Invalid token", debug=e
            )

        user = await self.repo.get(user_id)
        if user is None:
            raise TaskifyException(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid token",
                "User for provided token does not exist",
            )

        if not user.is_active:
            raise TaskifyException(
                status.HTTP_401_UNAUTHORIZED, "Invalid token", "User inactive"
            )

        return user

    async def logout(self):
        response = Response(status_code=204)
        response.delete_cookie(key=settings.AUTH_COOKIE_NAME)
        return response

    async def reset_password(self, credentials: ResetPasswordCredentials, user: User):
        is_valid, _ = self.password_helper.verify_and_update(
            credentials.old_password, user.hashed_password
        )
        if not is_valid:
            raise TaskifyException(
                status.HTTP_400_BAD_REQUEST,
                "Incorrect password",
                "Your current password is incorect. Try again",
            )
        new_password_hash = self.password_helper.hash(credentials.new_password)
        return await self.repo.update(user, {"hashed_password": new_password_hash})

    async def forgot_password(self, email: str):
        user = await self.repo.get_by_email(email)
        if user is None:
            raise TaskifyException(
                status.HTTP_400_BAD_REQUEST,
                "User does not exits",
                "User with provided email does not exist",
            )

        token = self._encode_jwt_token(
            {"sub": user.email},
            settings.JWT_RESET_TOKEN_MAX_AGE,
            settings.JWT_RESET_TOKEN_AUDIENCE,
        )

        return token

    async def verify_forgotten_password(self, new_password: str, token: str):
        error = lambda e: TaskifyException(
            status.HTTP_400_BAD_REQUEST,
            "Invalid reset token",
            "Invalid reset token",
            debug=e,
        )
        try:
            decoded_token = self._decode_jwt_token(
                token, settings.JWT_RESET_TOKEN_AUDIENCE
            )
        except jwt.DecodeError as e:
            raise error(e)

        email = decoded_token.get("sub", None)
        if email is None:
            raise error(None)

        user = await self.repo.get_by_email(email)

        if user is None:
            raise error(None)

        new_hashed_password = self.password_helper.hash(new_password)

        return await self.repo.update(user, {"hashed_password": new_hashed_password})

    async def oauth_callback(self, token: OAuth2Token, state: str, client: BaseOAuth2):
        account_id, account_email = await client.get_id_email(token["access_token"])
        if account_email is None:
            raise TaskifyException(
                status.HTTP_400_BAD_REQUEST,
                "Invalid Login",
                "OAuth2 don`t provide email",
            )

        try:
            jwt.decode(
                state,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                audience=settings.JWT_STATE_TOKEN_AUDIENCE,
            )
        except jwt.DecodeError as e:
            raise TaskifyException(
                status.HTTP_400_BAD_REQUEST,
                "Invalid token",
                "Can not decode state token",
                debug=e,
            )

        oauth_account_dict = {
            "oauth_name": client.name,
            "access_token": token["access_token"],
            "account_id": account_id,
            "account_email": account_email,
            "expires_at": token.get("expires_at", None),
            "refresh_token": token.get("refresh_token", None),
        }

        # Check if user with same oauth provider exist
        user = await self.oauth_repo.get_user_by_oauth(client.name, account_id)
        if user is None:
            # Check if user with email exist
            user = await self.repo.get_by_email(account_email)
            if user is None:
                user_payload = UserCreate(
                    email=account_email, password=self.password_helper.generate()
                )
                # Signup User
                user = await self.signup(user_payload, True)
                # Add User OAuthAccount
                user = await self.oauth_repo.add_account(user, oauth_account_dict)
            else:
                # Add OAuth account to user wich already exist
                user = await self.oauth_repo.add_account(user, oauth_account_dict)

        # Update OAuth account
        for existing_oauth_account in user.oauth_accounts:
            if (
                existing_oauth_account.account_id == account_id
                and existing_oauth_account.oauth_name == client.name
            ):
                user = await self.oauth_repo.update_account(
                    user, existing_oauth_account, oauth_account_dict
                )

        return self._create_login_response(user)

    async def remove_oauth(self, id: uuid.UUID, user: User):
        account = await self.oauth_repo.get(id)
        if account is None:
            raise TaskifyException(
                status.HTTP_404_NOT_FOUND,
                "OAuth Account not found",
                "OAuth account with such name does not exits",
            )
        if account not in user.oauth_accounts:
            raise TaskifyException(
                status.HTTP_403_FORBIDDEN,
                "This account not associated with user",
                f"OAuth Account not asociated with user {user.email}",
            )
        await self.oauth_repo.delete(account)

    def _create_login_response(self, user: User) -> Response:
        response = Response(status_code=204)
        token = self._encode_jwt_token(
            {"sub": str(user.id)},
            settings.JWT_AUTH_TOKEN_MAX_AGE,
            settings.JWT_AUTH_TOKEN_AUDIENCE,
        )
        response.set_cookie(key=settings.AUTH_COOKIE_NAME, value=token)
        return response

    def _encode_jwt_token(
        self, payload: dict[str, Any], max_age: int, audience: list[str] | None = None
    ):
        payload_dict = payload.copy()

        payload_dict.update(
            {
                "exp": datetime.now(UTC) + timedelta(seconds=max_age),
                "iat": datetime.now(UTC),
                "aud": audience,
            }
        )

        return jwt.encode(
            payload=payload_dict,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def _decode_jwt_token(
        self, token: str, audience: list[str] | None = None
    ) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                [settings.JWT_ALGORITHM],
                audience=audience,
            )
        except jwt.DecodeError as e:
            raise TaskifyException(
                status.HTTP_401_UNAUTHORIZED, "Invalid token", debug=e
            )

        return payload

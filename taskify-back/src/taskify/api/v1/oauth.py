from datetime import datetime, UTC, timedelta
from typing import Any
import uuid
from fastapi import Depends, Request
import jwt
from taskify.api.deps import auth_required, get_auth_service, AuthService
from taskify.models.auth import User
from taskify.schemas.auth import OAuth2AuthorizeResponse
from taskify.utils.cbv import Controller
from httpx_oauth.clients.github import GitHubOAuth2
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import OAuth2Token
from taskify.config import settings

github_oauth_client = GitHubOAuth2(
    settings.GITHUB_CLIENT_ID, settings.GITHUB_SECRET_KEY
)


def generate_state_token(payload: dict[str, Any]):
    payload["aud"] = settings.JWT_STATE_TOKEN_AUDIENCE
    payload["iat"] = datetime.now(UTC)
    payload["exp"] = datetime.now(UTC) + timedelta(
        seconds=settings.JWT_STATE_TOKEN_MAX_AGE
    )
    return jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)


class OAuthController(Controller):
    prefix = "/oauth"
    tags = ["Auth", "OAuth"]

    service: AuthService = Depends(get_auth_service)

    @Controller.get("/github/login", response_model=OAuth2AuthorizeResponse)
    async def github_login(self, request: Request):
        state_data: dict[str, str] = {}
        state = generate_state_token(state_data)

        authorization_url = await github_oauth_client.get_authorization_url(
            redirect_uri=settings.GITHUB_CALLBACK_URL
            or str(request.url_for("github-callback")),
            state=state,
        )
        return OAuth2AuthorizeResponse(authorization_url=authorization_url)

    @Controller.get("/github/callback", name="github-callback")
    async def github_callback(
        self,
        request: Request,
        access_token_state: tuple[OAuth2Token, str] = Depends(
            OAuth2AuthorizeCallback(
                github_oauth_client, redirect_url=settings.GITHUB_CALLBACK_URL
            )
        ),
    ):
        token, state = access_token_state
        return await self.service.oauth_callback(token, state, github_oauth_client)

    @Controller.delete("/{oauth_id}", status_code=204)
    async def remove_oauth_account(
        self, oauth_id: uuid.UUID, user: User = Depends(auth_required)
    ):
        await self.service.remove_oauth(oauth_id, user)

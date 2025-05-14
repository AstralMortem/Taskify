from fastapi import APIRouter, Body, Depends
from taskify.api.deps import auth_required, get_auth_service, AuthService
from taskify.schemas.auth import ForgotPassword, LoginCredentials, ResetPasswordCredentials
from taskify.schemas.user import UserCreate, UserRead
from taskify.utils.cbv import Controller


class AuthController(Controller):
    prefix = "/auth"
    tags = ["Auth"]
    resource = 'auth'

    service: AuthService = Depends(get_auth_service)

    @Controller.post("/login")
    async def password_login(self, credentials: LoginCredentials):
        return await self.service.login(credentials)

    @Controller.post("/logout", dependencies=[Depends(auth_required)])
    async def logout(self):
        return await self.service.logout()

    @Controller.post("/signup", response_model=UserRead)
    async def signup(self, payload: UserCreate):
        return await self.service.signup(payload, True)
    
    @Controller.post('/reset-password', response_model=UserRead)
    async def reset_password(self, credentials: ResetPasswordCredentials, user = Depends(auth_required)):
        return await self.service.reset_password(credentials, user)

    @Controller.post('/forgot-password', status_code=204 )
    async def forgot_password(self, credentials: ForgotPassword):
        token = await self.service.forgot_password(credentials.email)

    @Controller.post('/forgot-password-verify', status_code=204)
    async def verify_forgotten_password(self, new_password: str = Body(...), token: str = Body(...)):
        await self.service.verify_forgotten_password(new_password, token)
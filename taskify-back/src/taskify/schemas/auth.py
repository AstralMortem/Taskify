import uuid
from pydantic import BaseModel


class LoginCredentials(BaseModel):
    email: str
    password: str

class ResetPasswordCredentials(BaseModel):
    old_password: str
    new_password: str

class ForgotPassword(BaseModel):
    email: str

class OAuth2AuthorizeResponse(BaseModel):
    authorization_url: str


class OAuthRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    oauth_name: str
    account_id: str
    account_email: str
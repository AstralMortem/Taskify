from taskify.schemas.auth import OAuthRead
from .base import CreateSchema, ReadSchema, UpdateSchema
import uuid


class UserCreate(CreateSchema):
    email: str
    username: str | None = None
    full_name: str | None = None
    password: str
    role_id: int | None = None


class UserUpdate(UpdateSchema):
    email: str | None = None
    username: str | None = None
    full_name: str | None = None


class UserRead(ReadSchema):
    id: uuid.UUID
    email: str
    username: str | None
    full_name: str | None
    avatar: str | None
    role_id: int
    is_active: bool

    oauth_accounts: list[OAuthRead] = []

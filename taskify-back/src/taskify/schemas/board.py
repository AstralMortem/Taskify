import uuid
from .base import CreateSchema, ReadSchema, UpdateSchema


class BoardMemeber(ReadSchema):
    id: uuid.UUID
    email: str
    username: str
    full_name: str | None
    avatar: str | None

class BoardCreate(CreateSchema):
    title: str
    description: str | None = None
    background: str | None = None
    owner_id: uuid.UUID | None = None


class BoardUpdate(UpdateSchema):
    title: str | None = None
    description: str | None = None
    background: str | None = None


class BoardRead(ReadSchema):
    id: uuid.UUID
    title: str
    description: str | None
    background: str | None
    owner_id: uuid.UUID
    is_public: bool = False
    public_hash: str | None = None
    members: list[BoardMemeber]
    owner: BoardMemeber

class PublicBoardUpdate(UpdateSchema):
    is_public:bool
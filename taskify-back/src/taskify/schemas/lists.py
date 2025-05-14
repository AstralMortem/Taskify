from .base import ReadSchema, CreateSchema, UpdateSchema
import uuid


class ListRead(ReadSchema):
    id: uuid.UUID
    title: str
    position: int
    board_id: uuid.UUID


class ListCreate(CreateSchema):
    title: str
    position: int | None = None


class ListUpdate(UpdateSchema):
    title: str | None = None

from datetime import datetime
import uuid
from .base import CreateSchema, UpdateSchema, ReadSchema


class CardRead(ReadSchema):
    title: str
    description: str
    position: int
    list_id: uuid.UUID
    assigned_to_id: uuid.UUID | None
    due_date: datetime | None
    is_completed: bool


class CardCreate(CreateSchema):
    title: str
    description: str
    position: int | None = None
    assigned_to_id: uuid.UUID | None = None
    due_date: datetime | None = None
    is_completed: bool = False


class CardUpdate(UpdateSchema):
    title: str | None = None
    description: str | None = None
    assigned_to_id: uuid.UUID | None = None
    list_id: uuid.UUID | None = None
    due_date: datetime | None = None
    is_completed: bool | None = None

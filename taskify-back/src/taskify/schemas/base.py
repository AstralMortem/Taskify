from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime


class ReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

from typing import Any
from fastapi import UploadFile
from pydantic import BaseModel, Field
from taskify.config import settings


def get_url_without_domain(model: dict[str, Any]):
    return (
        f"{model['bucket']}/{model['object_key']}?{model['domain_url'].split('?')[1]}"
    )


class FileCreate:
    filepath: str
    file: UploadFile


class FileUploadResponse(BaseModel):
    filename: str
    bucket: str = settings.BUCKET_NAME
    object_key: str
    domain_url: str
    size: int = 0
    url: str = Field(default_factory=get_url_without_domain)

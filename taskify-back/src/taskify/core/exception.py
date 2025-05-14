from typing import Mapping
from fastapi.responses import JSONResponse
from taskify.config import settings
from starlette import status


class TaskifyException(Exception):
    def __init__(
        self,
        code: int,
        title: str,
        description: str | None = None,
        debug: Exception | str | None = None,
        headers: Mapping[str, str] | None = None,
    ):
        self.code = code
        self.title = title
        self.description = description
        self.debug = str(debug)
        self.headers = headers

    def to_response(self):
        payload = {
            "code": self.code,
            "title": self.title,
            "description": self.description,
        }

        if settings.DEBUG:
            payload["debug"] = self.debug

        return JSONResponse(
            content=payload, status_code=self.code, headers=self.headers
        )


__all__ = ["TaskifyException", "status"]

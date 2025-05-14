import uuid
from fastapi_filter.contrib.sqlalchemy import Filter
from taskify.models.auth import User
from taskify.models.board import Board, Card, List


class BoardFilter(Filter):
    owner_id: uuid.UUID | None = None
    order_by: list[str] = ["+is_stared", "-updated_at"]

    class Constants(Filter.Constants):
        model = Board


class ListFilter(Filter):
    board_id: uuid.UUID | None = None
    order_by: list[str] = ["+position"]

    class Constants(Filter.Constants):
        model = List


class CardFilter(Filter):
    list_id: uuid.UUID | None = None
    order_by: list[str] = ["+position"]

    class Constants(Filter.Constants):
        model = Card


class UserFilter(Filter):
    email__like: str | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):
        model = User

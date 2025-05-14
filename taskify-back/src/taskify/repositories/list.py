from fastapi import Depends
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession

from taskify.core.db import get_session
from taskify.schemas.filters import ListFilter
from .base import BaseRepository
from taskify.models.board import List
import uuid


class ListRepository(BaseRepository[List, uuid.UUID]):
    model = List

    async def get_board_list(self, board_id: uuid.UUID, params: Params, **kwargs):
        filter = ListFilter(board_id=board_id)
        return await self.get_many(params, filter)

    async def reorder_lists(
        self, list_dict: dict[uuid.UUID, List], list_order: list[uuid.UUID]
    ):
        for idx, list_id in enumerate(list_order):
            list_obj = list_dict[list_id]
            list_obj.position = idx
            self.session.add(list_obj)
        await self.session.commit()


async def get_list_repository(session: AsyncSession = Depends(get_session)):
    return ListRepository(session)

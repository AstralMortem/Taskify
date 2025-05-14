from operator import index
from textwrap import indent
from fastapi_pagination import Page, Params
from taskify.core.exception import TaskifyException, status

from taskify.schemas.filters import ListFilter
from taskify.schemas.lists import ListCreate, ListUpdate
from .base import BaseService
from taskify.repositories.list import ListRepository
from taskify.models.board import Board, List
import uuid


class ListService(BaseService[ListRepository, List, uuid.UUID, ListCreate, ListUpdate]):
    async def get_board_lists(self, board_id: uuid.UUID, params: Params, public_hash: str | None = None) -> Page[List]:
        filter = ListFilter(board_id=board_id)
        return await self.repo.get_many(params, filter)

    async def create(self, payload: ListCreate, **kwargs) -> List:
        dump = payload.model_dump()
        board: Board = kwargs.get("board", None)
        if "position" not in dump or dump["position"] is None:
            dump["position"] = len(board.lists)
        dump["board_id"] = board.id

        return await self.repo.create(dump)

    async def reorder_lists(
        self, board: Board, list_order: list[uuid.UUID], params: Params
    ) -> Page[List]:
        board_id = board.id
        id_map = {item.id: item for item in board.lists}
        list_dict = {id_map[i].id: id_map[i] for i in list_order if i in id_map}

        for list_id in list_order:
            if list_id not in list_dict or list_dict[list_id].board_id != board_id:
                raise TaskifyException(
                    status.HTTP_400_BAD_REQUEST,
                    f"List {list_id} does not belong to {board.id} board",
                )
        await self.repo.reorder_lists(list_dict, list_order)
        return await self.get_board_lists(board_id, params)

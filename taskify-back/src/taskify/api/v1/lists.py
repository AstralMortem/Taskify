import uuid
from fastapi import Body, Depends
from fastapi_pagination import Page, Params

from taskify.api.deps import get_board_service, get_list_service
from taskify.models.auth import User
from taskify.schemas.lists import ListCreate, ListRead, ListUpdate
from taskify.schemas.rbac import Action
from taskify.services.boards import BoardService
from taskify.services.lists import ListService
from taskify.utils.cbv import Controller
from taskify.utils.permissions import HasPermission


class ListController(Controller):
    prefix = "/lists"
    tags = ["Lists"]
    resource = "lists"

    service: ListService = Depends(get_list_service)
    board_service: BoardService = Depends(get_board_service)

    @Controller.get("/board/{board_id}", response_model=Page[ListRead])
    async def get_board_lists(
        self,
        board_id: uuid.UUID,
        params: Params = Depends(),
        user: User = Depends(HasPermission(Action.READ)),
    ):
        return await self.service.get_board_lists(board_id, params)

    @Controller.get("/board/public/{board_hash}", response_model=Page[ListRead])
    async def get_public_lists(self, board_hash: str, params: Params = Depends()):
        board = await self.board_service.get_public_board(board_hash)
        return await self.service.get_board_lists(board.id, params)

    @Controller.post("/board/{board_id}", response_model=ListRead)
    async def create_list_in_board(
        self,
        board_id: uuid.UUID,
        payload: ListCreate,
        user: User = Depends(HasPermission(Action.CREATE)),
    ):
        board = await self.board_service.get(board_id)
        return await self.service.create(payload, board=board)

    @Controller.get("/{list_id}", response_model=ListRead)
    async def get_list(
        self,
        list_id: uuid.UUID,
        user: User = Depends(HasPermission(Action.READ)),
    ):
        return await self.service.get(list_id)

    @Controller.patch("/{list_id}", response_model=ListRead)
    async def patch_list(
        self,
        list_id: uuid.UUID,
        payload: ListUpdate,
        user: User = Depends(HasPermission(Action.UPDATE)),
    ):
        return await self.service.patch(list_id, payload)

    @Controller.delete("/{list_id}", status_code=204)
    async def delete_list(
        self,
        list_id: uuid.UUID,
        user: User = Depends(HasPermission(Action.DELETE)),
    ):
        return await self.service.delete(list_id)

    @Controller.post("/board/{board_id}/reorder", response_model=Page[ListRead])
    async def reorder_list(
        self,
        board_id: uuid.UUID,
        list_order: list[uuid.UUID] = Body(...),
        params: Params = Depends(),
        user: User = Depends(HasPermission(Action.UPDATE)),
    ):
        board = await self.board_service.get(board_id)
        return await self.service.reorder_lists(board, list_order, params)

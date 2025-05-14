import uuid
from fastapi import Depends
from fastapi_pagination import Page, Params

from taskify.api.deps import (
    get_board_service,
    get_user_service
)
from taskify.models.auth import User
from taskify.schemas.board import (
    BoardCreate,
    BoardRead,
    BoardUpdate,
    PublicBoardUpdate,
)
from taskify.services.boards import BoardService
from taskify.services.users import UserService
from taskify.utils.cbv import Controller
from taskify.schemas.rbac import Action
from taskify.utils.permissions import HasPermission

class BoardController(Controller):
    prefix = "/boards"
    tags = ["Boards"]
    resource = "boards"

    service: BoardService = Depends(get_board_service)
    user_service: UserService = Depends(get_user_service)

    @Controller.get("/", response_model=Page[BoardRead])
    async def get_user_boards(
        self,
        params: Params = Depends(),
        user: User = Depends(HasPermission(Action.READ)),
    ):
        return await self.service.get_user_boards(user.id, params)

    @Controller.get("/membered/all", response_model=Page[BoardRead])
    async def get_a_membered_board(
        self,
        params: Params = Depends(),
        user: User = Depends(HasPermission(Action.READ)),
    ):
        return await self.service.get_membered_boards(user, params)

    @Controller.post("/", response_model=BoardRead)
    async def create_board(
        self, payload: BoardCreate, user: User = Depends(HasPermission(Action.CREATE))
    ):
        payload.owner_id = user.id
        return await self.service.create(payload)

    @Controller.get("/{board_id}", response_model=BoardRead)
    async def get_board(
        self, board_id: uuid.UUID, user: User = Depends(HasPermission(Action.READ))
    ):
        return await self.service.get(board_id)

    @Controller.patch("/{board_id}", response_model=BoardRead)
    async def patch_board(
        self,
        board_id: uuid.UUID,
        payload: BoardUpdate,
        user: User = Depends(HasPermission(Action.UPDATE)),
    ):
        return await self.service.patch(board_id, payload, owner_id=user.id)

    @Controller.delete("/{board_id}", status_code=204)
    async def delete_board(
        self, board_id: uuid.UUID, user: User = Depends(HasPermission(Action.DELETE))
    ):
        return await self.service.delete(board_id, False, owner_id=user.id)

    @Controller.post("/{board_id}/members/{member_id}", response_model=BoardRead)
    async def add_board_member(
        self,
        board_id: uuid.UUID,
        member_id: uuid.UUID,
        user: User = Depends(HasPermission(Action.UPDATE)),
    ):
        member = await self.user_service.get(member_id)
        return await self.service.add_board_member(
            board_id, owner_id=user.id, member=member
        )

    @Controller.delete("/{board_id}/members/{member_id}", response_model=BoardRead)
    async def remove_board_member(
        self,
        board_id: uuid.UUID,
        member_id: uuid.UUID,
        user: User = Depends(HasPermission(Action.UPDATE)),
    ):
        member = await self.user_service.get(member_id)
        return await self.service.remove_board_member(
            board_id, owner_id=user.id, member=member
        )

    @Controller.patch("/{board_id}/change_public", response_model=BoardRead)
    async def update_publicity(
        self,
        board_id: uuid.UUID,
        is_public: PublicBoardUpdate,
        user: User = Depends(HasPermission(Action.UPDATE)),
    ):
        return await self.service.change_board_publicity(
            board_id, is_public.is_public, user
        )

    @Controller.get("/public/{board_hash}", response_model=BoardRead)
    async def get_public_board(self, board_hash: str):
        return await self.service.get_public_board(board_hash)

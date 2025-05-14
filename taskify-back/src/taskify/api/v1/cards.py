import uuid
from fastapi import APIRouter, Body, Depends
from fastapi_pagination import Page, Params

from taskify.api.deps import (
    auth_required,
    get_board_service,
    get_card_service,
    get_list_service,
    get_user_service,
)
from taskify.core.exception import TaskifyException, status
from taskify.schemas.cards import CardCreate, CardRead, CardUpdate
from taskify.schemas.rbac import Action
from taskify.services.boards import BoardService
from taskify.services.cards import CardService
from taskify.services.lists import ListService
from taskify.services.users import UserService
from taskify.utils.cbv import Controller
from taskify.utils.permissions import HasPermission


class CardController(Controller):
    prefix = "/cards"
    tags = ["Cards"]
    resource = 'cards'

    service: CardService = Depends(get_card_service)
    list_service: ListService = Depends(get_list_service)
    board_service: BoardService = Depends(get_board_service)
    user_service: UserService = Depends(get_user_service)

    @Controller.get("/{card_id}", response_model=CardRead)
    async def get_card(self, card_id: uuid.UUID, user=Depends(HasPermission(Action.READ))):
        return await self.service.get(card_id)

    @Controller.get("/list/{list_id}", response_model=Page[CardRead])
    async def get_list_cards(self, list_id: uuid.UUID, params: Params = Depends(), user=Depends(HasPermission(Action.READ))):
        return await self.service.get_list_cards(list_id, params)
    
    @Controller.get('/list/{list_id}/public/{board_hash}', response_model=Page[CardRead])
    async def get_public_list_cards(self, list_id: uuid.UUID, board_hash: str, params: Params = Depends()):

        board = await self.board_service.get_public_board(board_hash)
        if not any(list_id == l.id for l in board.lists):
            raise TaskifyException(status.HTTP_403_FORBIDDEN, "Access Denied", "This list not in public board")

        return await self.service.get_list_cards(list_id, params)

    @Controller.post("/list/{list_id}", response_model=CardRead)
    async def create_card(self, list_id: uuid.UUID, payload: CardCreate, user=Depends(HasPermission(Action.CREATE))):
        list = await self.list_service.get(list_id)
        # Check if card assigned to user, and user exist
        if hasattr(payload, "assigned_to_id") and payload.assigned_to_id is not None:
            await self.user_service.get(payload.assigned_to_id)

        return await self.service.create(payload, list=list)

    @Controller.patch("/{card_id}", response_model=CardRead)
    async def patch_card(self, card_id: uuid.UUID, payload: CardUpdate, user=Depends(HasPermission(Action.UPDATE))):
        if payload.assigned_to_id is not None:
            await self.user_service.get(payload.assigned_to_id)
        if payload.list_id is not None:
            await self.list_service.get(payload.list_id)

        return await self.service.patch(card_id, payload)

    @Controller.delete("/{card_id}", status_code=204)
    async def delete_card(self, card_id: uuid.UUID, user=Depends(HasPermission(Action.DELETE))):
        return await self.service.delete(card_id)

    @Controller.post("/{card_id}/move", response_model=CardRead)
    async def move_card(
        self,
        card_id: uuid.UUID,
        target_list_id: uuid.UUID = Body(...),
        position: int = Body(...),
        user=Depends(HasPermission(Action.UPDATE))
    ):
        list = await self.list_service.get(target_list_id)
        return await self.service.move_card(card_id, list, position)

    @Controller.post("/list/{list_id}/reorder", response_model=Page[CardRead])
    async def reorder_cards(
        self,
        list_id: uuid.UUID,
        card_order: list[uuid.UUID] = Body(...),
        params: Params = Depends(),
        user=Depends(HasPermission(Action.UPDATE))
    ):
        list = await self.list_service.get(list_id)
        return await self.service.reorder_cards(list, card_order, params)

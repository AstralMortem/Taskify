import uuid

from fastapi_pagination import Page, Params
from taskify.core.exception import TaskifyException, status
from taskify.models.auth import User
from taskify.models.board import Board
from taskify.schemas.board import BoardCreate, BoardUpdate
from taskify.schemas.filters import BoardFilter
from .base import BaseService
from taskify.repositories.board import BoardRepository


class BoardService(
    BaseService[BoardRepository, Board, uuid.UUID, BoardCreate, BoardUpdate]
):
    async def get_user_boards(self, user_id: uuid.UUID, params: Params) -> Page[Board]:
        filter = BoardFilter(owner_id=user_id)
        return await self.repo.get_many(params, filter)

    async def patch(self, id: uuid.UUID, payload: BoardUpdate, **kwargs) -> Board:
        instance = await self.get(id)

        if instance.owner_id != kwargs.get("owner_id", ""):
            if not any([kwargs.get("owner_id") == m.id for m in instance.members]):
                raise TaskifyException(
                    status.HTTP_403_FORBIDDEN,
                    "Access Denied",
                    "You can update only own boards",
                )

        dump = payload.model_dump(
            exclude_defaults=True, exclude_unset=True, exclude_none=True
        )
        return await self._update(instance, dump, **kwargs)

    async def delete(
        self, id: uuid.UUID, with_return: bool = False, **kwargs
    ) -> Board | None:
        instance = await self.get(id)
        if instance.owner_id != kwargs.get("owner_id", 0):
            raise TaskifyException(
                status.HTTP_403_FORBIDDEN,
                "Access Denied",
                "You can delete only own boards",
            )
        return await self.repo.delete(instance)

    async def add_board_member(self, id: uuid.UUID, owner_id: uuid.UUID, member: User):
        instance = await self.get(id)
        if instance.owner_id != owner_id:
            raise TaskifyException(
                status.HTTP_403_FORBIDDEN,
                "Access Denied",
                "You can update only own boards",
            )
        return await self.repo.add_member(instance, member)

    async def remove_board_member(
        self, id: uuid.UUID, owner_id: uuid.UUID, member: User
    ):
        instance = await self.get(id)
        if instance.owner_id != owner_id:
            raise TaskifyException(
                status.HTTP_403_FORBIDDEN,
                "Access Denied",
                "You can update only own boards",
            )
        return await self.repo.remove_member(instance, member)

    async def get_membered_boards(self, member: User, params: Params) -> Page[Board]:
        return await self.repo.get_membered_board(member, params)

    async def get_public_board(self, hash: str) -> Board:
        instance = await self.repo.get_public_board(hash)
        if instance is None:
            raise TaskifyException(
                status.HTTP_404_NOT_FOUND,
                "Board not found",
                "Board does not exist or already private",
            )
        return instance

    async def change_board_publicity(
        self, id: uuid.UUID, is_public: bool, user: User
    ) -> Board:
        instance = await self.get(id)
        if instance.owner_id != user.id:
            raise TaskifyException(
                status.HTTP_403_FORBIDDEN,
                "Access Denied",
                "Only owner can change board publicity",
            )
        return await self.repo.update_board_publicity(instance, is_public)

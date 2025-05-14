import secrets
from fastapi import Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from taskify.core.db import get_session
from taskify.models.auth import User
from .base import BaseRepository
from taskify.models.board import Board, BoardMemberRel
from sqlalchemy import select
from typing import Sequence
import uuid


class BoardRepository(BaseRepository[Board, uuid.UUID]):
    model = Board

    async def add_member(self, instance: Board, member: User) -> Board:
        if member not in instance.members:
            instance.members.append(member)
            await self.session.commit()
            await self.session.refresh(instance)
        return instance

    async def remove_member(self, instance: Board, member: User) -> Board:
        if member in instance.members:
            instance.members.remove(member)
            await self.session.commit()
            await self.session.refresh(instance)
        return instance
    
    async def get_membered_board(self, member: User, params: Params) -> Page[Board]:
        qs = select(self.model).join(BoardMemberRel, BoardMemberRel.board_id == self.model.id).where(BoardMemberRel.user_id == member.id)
        return await paginate(self.session, qs, params)
    
    async def update_board_publicity(self,instance: Board, is_public: bool) -> Board:
        if is_public is True:
            payload = {
                'is_public': is_public,
                "public_hash": self._generate_public_hash()
            }
        else:
            payload = {'is_public': is_public}
        return await self.update(instance, payload)
    
    def _generate_public_hash(self):
        return secrets.token_urlsafe(16)

    async def get_public_board(self, hash:str) -> Board | None:
        qs = select(self.model).where(self.model.public_hash == hash, self.model.is_public == True).limit(1)
        return await self.session.scalar(qs)

async def get_board_repository(session: AsyncSession = Depends(get_session)):
    return BoardRepository(session)

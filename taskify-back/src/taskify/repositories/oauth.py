from typing import Any
import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from taskify.core.db import get_session
from taskify.models.auth import User
from taskify.models.oauth import OAuthAccount
from .base import BaseRepository

class OAuthRepository(BaseRepository[OAuthAccount, uuid.UUID]):
    model = OAuthAccount

    async def get_user_by_oauth(self, oauth_name: str, account_id: str) -> User | None:
        qs = select(User).join(self.model).where(self.model.oauth_name == oauth_name, OAuthAccount.account_id == account_id)
        res = await self.session.execute(qs)
        return res.unique().scalar_one_or_none()
    
    async def update_account(self, user: User, oauth: OAuthAccount, payload: dict[str, Any]):
        for key, val in payload.items():
            setattr(oauth, key, val)
        self.session.add(oauth)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def add_account(self, user: User, payload: dict):
        oauth_instance = self.model(**payload)
        self.session.add(oauth_instance)
        user.oauth_accounts.append(oauth_instance)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    

async def get_oauth_repository(session: AsyncSession = Depends(get_session)):
    return OAuthRepository(session)
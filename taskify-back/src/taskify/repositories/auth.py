from taskify.core.db import get_session
from .base import BaseRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from taskify.models.auth import User, Role, Permission
import uuid


class UserRepository(BaseRepository[User, uuid.UUID]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        return await self.get_by_field("email", email)


class RoleRepository(BaseRepository[Role, int]):
    model = Role


class PermissionRepository(BaseRepository[Permission, int]):
    model = Permission


async def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)


async def get_role_repository(session: AsyncSession = Depends(get_session)):
    return RoleRepository(session)


async def get_permission_repository(session: AsyncSession = Depends(get_session)):
    return PermissionRepository(session)

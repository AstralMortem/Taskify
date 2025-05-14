from fastapi_pagination import Page, Params

from taskify.schemas.filters import UserFilter
from taskify.schemas.storage import FileUploadResponse
from .base import BaseService
from taskify.repositories.auth import UserRepository
from taskify.schemas.user import UserCreate, UserUpdate
from taskify.models.auth import User
import uuid


class UserService(BaseService[UserRepository, User, uuid.UUID, UserCreate, UserUpdate]):
    


    async def filter_members(self,params: Params, user: User, email: str | None = None):
        if not email:
            users = []
            for board in user.boards:
                for member in board.members:
                    users.append(member)
            return Page[User].create(users, params=params, total=len(users))
        else:
            filter = UserFilter(email__like=email)
            return await self.repo.get_many(params,filter)


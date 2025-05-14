from taskify.schemas.rbac import Action
import uuid
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from taskify.api.deps import auth_required, get_user_service
from taskify.models.auth import User
from taskify.schemas.board import BoardMemeber
from taskify.schemas.user import UserRead, UserUpdate
from taskify.services.users import UserService
from taskify.utils.cbv import Controller
from taskify.utils.permissions import HasPermission

user_router = APIRouter(prefix="/users", tags=["Users"])


class UserController(Controller):
    prefix = "/users"
    tags = ["Users"]
    resource = 'users'

    service: UserService = Depends(get_user_service)

    @Controller.get("/me", response_model=UserRead)
    async def get_me(self, user: User = Depends(auth_required)):
        return user

    @Controller.patch("/me", response_model=UserRead)
    async def patch_me(self, payload: UserUpdate, user: User = Depends(auth_required)):
        dump = payload.model_dump(
            exclude_none=True, exclude_defaults=True, exclude_unset=True
        )
        return await self.service._update(user, dump)

    @Controller.get("/{user_id}", response_model=UserRead)
    async def get_user(self, user_id: uuid.UUID, user: User = Depends(HasPermission(Action.READ))):
        return await self.service.get(user_id)

    @Controller.get('/', response_model=Page[BoardMemeber])
    async def filter_users(self, params: Params = Depends(), user: User = Depends(HasPermission(Action.READ)), email: str | None = None, ):
        return await self.service.filter_members(params, user, email)
from fastapi import APIRouter
from .auth import AuthController
from .users import UserController
from .boards import BoardController
from .lists import ListController
from .cards import CardController
from .oauth import OAuthController
from .storage import FileStorageController

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(AuthController.as_router())
v1_router.include_router(UserController.as_router())
v1_router.include_router(BoardController.as_router())
v1_router.include_router(ListController.as_router())
v1_router.include_router(CardController.as_router())
v1_router.include_router(OAuthController.as_router())
v1_router.include_router(FileStorageController.as_router())

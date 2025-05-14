from fastapi import Depends
from fastapi.security import APIKeyCookie
from taskify.config import settings
from taskify.models.auth import User
from taskify.repositories.auth import get_user_repository, UserRepository
from taskify.repositories.board import BoardRepository, get_board_repository
from taskify.repositories.card import CardRepository, get_card_repository
from taskify.repositories.list import ListRepository, get_list_repository
from taskify.repositories.oauth import OAuthRepository, get_oauth_repository
from taskify.services.auth import AuthService
from taskify.services.boards import BoardService
from taskify.services.cards import CardService
from taskify.services.lists import ListService
from taskify.services.storage import StorageService
from taskify.services.users import UserService


async def get_auth_service(
    repo: UserRepository = Depends(get_user_repository),
    oauth_repo: OAuthRepository = Depends(get_oauth_repository),
) -> AuthService:
    return AuthService(repo, oauth_repo)


async def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


async def get_board_service(
    repo: BoardRepository = Depends(get_board_repository),
) -> BoardService:
    return BoardService(repo)


async def get_list_service(
    repo: ListRepository = Depends(get_list_repository),
) -> ListService:
    return ListService(repo)


async def get_card_service(repo: CardRepository = Depends(get_card_repository)):
    return CardService(repo)


async def get_file_storage(repo: UserRepository = Depends(get_user_repository)):
    return StorageService(repo)


cookie_schema = APIKeyCookie(name=settings.AUTH_COOKIE_NAME)


async def auth_required(
    token: str = Depends(cookie_schema),
    service: AuthService = Depends(get_auth_service),
) -> User:
    return await service.authenticate(token)



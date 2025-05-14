from fastapi import APIRouter
from taskify.config import settings
from .v1 import v1_router

global_router = APIRouter(prefix=settings.GLOBAL_ROUTER_PREFIX)
global_router.include_router(v1_router)

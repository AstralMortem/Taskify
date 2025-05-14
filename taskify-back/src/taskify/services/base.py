from fastapi_pagination import Params, Page
from fastapi_filter.base.filter import BaseFilterModel
from taskify.core.exception import TaskifyException, status
from taskify.repositories.base import ID, M, BaseRepository
from typing import Any, Generic, TypeVar
from taskify.schemas.base import CreateSchema, UpdateSchema

REPO = TypeVar("REPO", bound=BaseRepository)
CREATE_SCHEMA = TypeVar("CREATE_SCHEMA", bound=CreateSchema)
UPDATE_SCHEMA = TypeVar("UPDATE_SCHEMA", bound=UpdateSchema)


class BaseService(Generic[REPO, M, ID, CREATE_SCHEMA, UPDATE_SCHEMA]):
    def __init__(self, repository: REPO):
        self.repo = repository

    async def get(self, id: ID, **kwargs) -> M:
        instance = await self.repo.get(id, **kwargs)
        if instance is None:
            raise TaskifyException(
                status.HTTP_404_NOT_FOUND,
                f"{M.__class__.__name__} not found",
                "Item with provided ID not exist",
            )
        return instance

    async def list(
        self, pagination: Params, filter: BaseFilterModel, **kwargs
    ) -> Page[M]:
        return await self.repo.get_many(pagination, filter, **kwargs)

    async def create(self, payload: CREATE_SCHEMA, **kwargs) -> M:
        dump = payload.model_dump()
        return await self.repo.create(dump, **kwargs)

    async def put(self, id: ID, payload: UPDATE_SCHEMA, **kwargs) -> M:
        instance = await self.get(id)
        dump = payload.model_dump(exclude_unset=True, exclude_defaults=True)
        return await self._update(instance, dump, **kwargs)

    async def patch(self, id: ID, payload: UPDATE_SCHEMA, **kwargs) -> M:
        instance = await self.get(id)
        dump = payload.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude_none=True
        )
        return await self._update(instance, dump, **kwargs)

    async def delete(self, id: ID, with_return: bool = False, **kwargs) -> M | None:
        instance = await self.get(id)
        return await self.repo.delete(instance, with_return, **kwargs)

    async def _update(self, instance: M, payload: dict[str, Any], **kwargs) -> M:
        return await self.repo.update(instance, payload, **kwargs)

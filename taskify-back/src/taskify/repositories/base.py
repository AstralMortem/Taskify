from typing import Any, Generic, TypeVar
from taskify.models.base import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_filter.base.filter import BaseFilterModel

M = TypeVar("M", bound=BaseModel)
ID = TypeVar("ID")


class BaseRepository(Generic[M, ID]):
    model: type[M]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: ID, **kwargs) -> M | None:
        return await self.session.get(self.model, id)

    async def get_by_field(self, field: str, value: Any, **kwargs) -> M | None:
        qs = select(self.model).filter_by(**{field: value}).limit(1)
        return await self.session.scalar(qs)

    async def get_many(
        self, params: Params, filter: BaseFilterModel | None = None, **kwargs
    ) -> Page[M]:
        qs = select(self.model)
        if filter:
            qs = filter.filter(qs)
            qs = filter.sort(qs)

        return await paginate(self.session, qs, params)

    async def create(self, payload: dict[str, Any], **kwargs) -> M:
        instance = self.model(**payload)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: M, payload: dict[str, Any], **kwargs) -> M:
        for key, val in payload.items():
            setattr(instance, key, val)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(
        self, instance: M, with_return: bool = False, **kwargs
    ) -> M | None:
        await self.session.delete(instance)
        await self.session.commit()
        if with_return:
            return instance

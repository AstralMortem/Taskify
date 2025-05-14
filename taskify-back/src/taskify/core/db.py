from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from taskify.config import settings

engine = create_async_engine(settings.DATABASE_URL)
session_factory = async_sessionmaker(engine, class_=AsyncSession)


async def get_session():
    async with session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

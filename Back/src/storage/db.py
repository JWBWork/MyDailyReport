from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

# DATABASE_URL = "sqlite+aiosqlite:///:memory:"
DATABASE_URL = f"sqlite+aiosqlite:///{Path().resolve()}/test.db"

class Base(DeclarativeBase):
    __allow_unmapped__ = True
    pass

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables(*tables):
    async with engine.begin() as conn:
        # for table in tables:
        #     await conn.run_sync(table.__table__.create)
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

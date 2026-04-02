import os
from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker,
    AsyncAttrs
)
from typing import AsyncGenerator, Annotated


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # three levels up
db_path = os.path.join(BASE_DIR, "sqlite.db")
DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def create_tables():
    from app.account.models import User, RefreshToken
    from app.converter.models import UserCredits, APIKey, CreditRequest
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

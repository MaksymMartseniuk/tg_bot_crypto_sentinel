from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.database.models import Base
from config_reader import config
from typing import AsyncIterable
import redis #on the future

_DATABASE=config.database.get_secret_value()

engine=create_async_engine(_DATABASE,echo=True)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session()->AsyncIterable[AsyncSession]:
    async with async_session() as session:
        yield session
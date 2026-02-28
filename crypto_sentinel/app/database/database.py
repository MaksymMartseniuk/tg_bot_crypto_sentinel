from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.database.models import Base
from config_reader import config
from typing import AsyncIterable
from redis.asyncio import Redis

_DATABASE=config.database.get_secret_value()
_REDIS_HOST=config.redis_host.get_secret_value()
_REDIS_PORT=config.redis_port.get_secret_value()
_REDIS_DB=config.redis_db.get_secret_value()

engine=create_async_engine(_DATABASE,
                           echo=True,
                           pool_size=10,
                           max_overflow=20)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

redis_client=Redis(
    host=_REDIS_HOST,
    port=_REDIS_PORT,
    db=_REDIS_DB,
    decode_responses=True)

async def init_db():
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session()->AsyncIterable[AsyncSession]:
    async with async_session() as session:
        yield session

async def dispose_db():
    """Dispose the database engine and close the Redis client."""
    await engine.dispose()
    await redis_client.close()
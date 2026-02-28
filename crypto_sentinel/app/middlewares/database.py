from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker,redis,http_session)-> None:
        self.session_pool = session_pool
        self.redis = redis
        self.http_session = http_session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["session"] = self.session_pool()
        data["redis"] = self.redis
        data["http_session"] = self.http_session
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)
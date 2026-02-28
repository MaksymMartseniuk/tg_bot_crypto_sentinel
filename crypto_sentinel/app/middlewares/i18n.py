from typing import Any, Dict, Optional
from aiogram.utils.i18n import SimpleI18nMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.requests import get_user

class I18nMiddleware(SimpleI18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        event_user: Optional[User] = data.get("event_from_user")
        if not event_user:
            return self.i18n.default_locale
        session: Optional[AsyncSession] = data.get("session")
        if not session:
            return self.i18n.default_locale
        db_user = await get_user(session,event_user.id)
        if db_user and db_user.language:
            return db_user.language
        return self.i18n.default_locale

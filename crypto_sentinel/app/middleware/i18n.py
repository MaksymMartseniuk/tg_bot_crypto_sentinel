from typing import Any, Dict, Optional
from aiogram.utils.i18n import SimpleI18nMiddleware
from aiogram.types import TelegramObject, User
from app.database.requests import get_user

class I18nMiddleware(SimpleI18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        event_from_user: Optional[User] = data.get("event_from_user")
        if not event_from_user:
            return self.i18n.default_locale

        user = data.get("user")
        if user:
            return user.language
        session = data.get("session")
        if session:
            db_user = await get_user(event_from_user.id, session)
            if db_user:
                return db_user.language
            
        return event_from_user.language_code or self.i18n.default_locale
from typing import Any, Dict, Optional
from aiogram.utils.i18n import SimpleI18nMiddleware
from aiogram.types import TelegramObject, User
from app.database.requests import get_user

class I18nMiddleware(SimpleI18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        pass
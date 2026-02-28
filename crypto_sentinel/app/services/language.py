from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.i18n import I18n, gettext as _
from app.database.requests import set_user_language

async def change_user_language(session: AsyncSession, tg_id: int, lang_code: str, i18n: I18n)->str:
    i18n.current_locale = lang_code
    await set_user_language(session, tg_id, lang_code)
    return (
        _("Language set to Ukrainian! 🇺🇦") if lang_code == "uk" 
        else _("Language set to English! 🇺🇸")
    )


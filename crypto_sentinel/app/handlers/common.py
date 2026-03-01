from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.i18n import gettext as _, I18n
from app.keyboards.builders import main_menu
from app.services.language import change_user_language

common_router = Router()
@common_router.callback_query(F.data.startswith("lang:"))
async def process_language_choice(callback: CallbackQuery, session:AsyncSession,i18n: I18n):
    lang, source, lang_code = callback.data.split(":")
    confirm_text = await change_user_language(session, callback.from_user.id, lang_code, i18n)
    await callback.message.edit_text(confirm_text)
    user = callback.from_user
    if user.username:
        display_name = f"@{user.username}"
    else:
        name_parts = [user.first_name, user.last_name]
        display_name = " ".join(filter(None, name_parts))

        if not display_name:
            display_name = f"User {user.id}"

    if source == "start":
        await callback.message.answer(
            _("Welcome {name}! How can I help you today?").format(name=display_name),
            reply_markup=main_menu()
        )
    else:
        await callback.message.answer(
            _("Settings updated."),
            reply_markup=main_menu()
        )
    await callback.answer()

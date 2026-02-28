from aiogram import Router,F
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from aiogram.handlers.callback_query import CallbackQuery
from app.database.requests import set_user
from app.keyboards.builders import main_menu
from app.keyboards.settings_kb import get_settings_kb
from app.database.requests import set_user_language
from aiogram.utils.i18n import gettext as _, I18n


user_router=Router()

@user_router.message(CommandStart())
async def cmd_start(message:Message,session: AsyncSession):
    await set_user(session, message.from_user.id,message.from_user.username)
    await message.answer("Choose language / Виберіть мову",reply_markup=get_settings_kb())

@user_router.callback_query(F.data.startswith("set_lang_"))
async def process_language_choice(callback: CallbackQuery, session:AsyncSession,i18n: I18n):
    lang_code = callback.data.split("_")[-1]
    i18n.current_locale = lang_code
    await set_user_language(session, callback.from_user.id, lang_code)
    await callback.message.edit_text(
        _("Language set to Ukrainian! 🇺🇦") if lang_code == "uk" 
        else _("Language set to English! 🇺🇸")
    )
    
    await callback.message.answer(
        _("Welcome ! How can I help you today?"),
        reply_markup=main_menu()
    )
    
    await callback.answer()

from aiogram import Router,F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.handlers.callback_query import CallbackQuery
from app.database.requests import set_user
from app.keyboards.builders import main_menu
from app.keyboards.settings_kb import get_settings_kb
from app.database.requests import set_user_language
from aiogram.utils.i18n import gettext as _


user_router=Router()

@user_router.message(CommandStart())
async def cmd_start(message:Message):
    await set_user(message.from_user.id,message.from_user.username)
    await message.answer("Choose language / Виберіть мову",reply_markup=get_settings_kb())

@user_router.callback_query(F.data.startswith("set_lang_"))
async def process_language_choice(callback: CallbackQuery, session):
    lang_code = callback.data.split("_")[-1]
    
    await set_user_language(session, callback.from_user.id, lang_code)
    await callback.message.edit_text(
        _("Language set to Ukrainian! 🇺🇦", locale=lang_code) if lang_code == "uk" 
        else _("Language set to English! 🇺🇸", locale=lang_code)
    )
    
    await callback.message.answer(
        _("Welcome ! How can I help you today?", locale=lang_code),
        reply_markup=main_menu()
    )
    
    await callback.answer()
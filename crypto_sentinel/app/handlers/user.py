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
    await message.answer("Виберіть мову / Choose language",reply_markup=get_settings_kb("start"))


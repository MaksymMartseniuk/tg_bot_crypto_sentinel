from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.database.requests import set_user
from app.keyboards.builders import main_menu

user_router=Router()

@user_router.message(CommandStart())
async def cmd_start(message:Message):
    await set_user(message.from_user.id,message.from_user.username)
    await message.answer(f"Hello {message.from_user.username}",reply_markup=main_menu())
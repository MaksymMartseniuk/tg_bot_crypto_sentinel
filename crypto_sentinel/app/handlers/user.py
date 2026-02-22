from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.database.requests import set_user

router=Router()

@router.message(CommandStart())
async def cmd_start(message:Message):
    await set_user(message.from_user.id,message.from_user.username)
    await message.reply(f"Hello {message.from_user.username}")
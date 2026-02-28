from aiogram import F,Router
from aiogram.types import Message
from app.keyboards.builders import main_menu
from app.keyboards.settings_kb import get_settings_kb

setting_router = Router()

@setting_router.message(F.text == "⚙️ Settings")
async def settings_menu(message: Message):
    await message.answer("Select an option to configure:", reply_markup=get_settings_kb())
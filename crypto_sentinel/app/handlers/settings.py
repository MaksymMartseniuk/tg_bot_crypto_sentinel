from aiogram import F,Router
from aiogram.types import Message
from app.keyboards.builders import main_menu
from app.keyboards.settings_kb import get_settings_kb
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

setting_router = Router()

@setting_router.message(F.text == __("⚙️ Settings"))
async def settings_menu(message: Message):
    await message.answer(_("Select an option to configure:"), reply_markup=get_settings_kb())
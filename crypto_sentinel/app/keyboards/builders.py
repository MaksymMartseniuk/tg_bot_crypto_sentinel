from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
from aiogram.utils.i18n import gettext as _

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=_("🔔 Add Alert")))
    builder.add(KeyboardButton(text=_("📋 My Alerts")))
    builder.add(KeyboardButton(text=_("📈 Live Prices")))
    builder.add(KeyboardButton(text=_("⚙️ Settings")))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🔔 Add Alert"))
    builder.add(KeyboardButton(text="📋 My Alerts"))
    builder.add(KeyboardButton(text="📈 Live Prices"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
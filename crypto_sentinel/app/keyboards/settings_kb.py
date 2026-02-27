
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


def get_settings_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data="set_lang_uk"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="set_lang_en")
        ]
    ])
    return builder

from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.i18n import gettext as _


def get_settings_kb(source: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("🇺🇦 Українська"), callback_data=f"lang:{source}:uk"),
            InlineKeyboardButton(text=_("🇺🇸 English"), callback_data=f"lang:{source}:en")
        ]
    ])
    return builder
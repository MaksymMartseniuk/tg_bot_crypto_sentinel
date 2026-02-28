
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.i18n import gettext as _


def get_settings_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=_("🇺🇦 Українська"), callback_data="set_lang_uk"),
            InlineKeyboardButton(text=_("🇺🇸 English"), callback_data="set_lang_en")
        ]
    ])
    return builder
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _

def get_popular_crypto_kb() -> ReplyKeyboardMarkup:
    popular_coins = ["BTC", "ETH", "SOL", "TON", "XRP", "DOGE"]
    builder=ReplyKeyboardBuilder()
    for coin in popular_coins:
        builder.button(text=coin)
    builder.button(text=_("❌ Cancel"))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True,input_field_placeholder=_("Enter symbol, e.g. BTC..."))
    
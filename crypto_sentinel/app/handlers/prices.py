from aiogram import F,Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from aiogram.filters import StateFilter
from aiogram.enums import ParseMode
from app.services.binance_api import get_crypto_price
from app.keyboards.price_kb import get_popular_crypto_kb
from app.keyboards.builders import main_menu
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

price_router=Router()

class PriceCheck(StatesGroup):
    waiting_for_symbol = State()

@price_router.message(StateFilter(None),F.text==__("📈 Live Prices"))
async def ask_for_symbol(message:Message,state:FSMContext):
    await message.answer(_("Which coin do you want to check? Enter symbol (e.g., BTC, ETH):"),reply_markup=get_popular_crypto_kb())
    await state.set_state(PriceCheck.waiting_for_symbol)

@price_router.message(PriceCheck.waiting_for_symbol,F.text==__("❌ Cancel"))
async def cancel_price_check(message:Message,state:FSMContext):
    await state.clear()
    await message.answer(_("Action cancelled."), reply_markup=main_menu())

@price_router.message(PriceCheck.waiting_for_symbol)
async def process_price_check(message:Message,state:FSMContext):
    symbol=message.html_text.upper().strip()
    price= await get_crypto_price(symbol=symbol)
    if price:
        formatted_price = f"{price:,.2f}" if price > 1 else f"{price:.6f}"
        await message.answer(
            _("🚀 <b>{symbol}</b> Price: <code>${price}</code>").format(
                symbol=symbol, 
                price=formatted_price
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu()
        )
    else:
        await message.answer(
            _("❌ Could not find <b>{symbol}</b>. Try again.").format(symbol=symbol),
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu()
        )
    await state.clear()



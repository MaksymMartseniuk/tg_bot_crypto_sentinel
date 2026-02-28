import aiohttp
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession
from app.keyboards.builders import main_menu
from app.keyboards.price_kb import get_popular_crypto_kb
from app.services.binance_api import get_crypto_price
from app.database.requests import add_alert, get_user_alerts
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

alerts_router=Router()

class CreateAlert(StatesGroup):
    waiting_for_symbol=State()
    waiting_for_price=State()


@alerts_router.message(F.text==__("📋 My Alerts"))
async def show_user_alerts(message: Message, session: AsyncSession):
    alerts_user = await get_user_alerts(session, message.from_user.id)
    if alerts_user:
        alert_messages = []
        for alert in alerts_user:
            emoji = "📈" if getattr(alert, 'direction', 'UP') == "UP" else "📉"
            status = _("🟢 Active") if alert.is_active else _("⚪ Triggered")
            msg = _("{emoji} <b>{symbol}</b> - Target: <code>${price:,.2f}</code>\n"
                    "Status: {status}").format(
                        emoji=emoji, 
                        symbol=alert.symbol, 
                        price=alert.target_price, 
                        status=status
                    )
            alert_messages.append(msg)
        await message.answer(
            _("Your Active Alerts:\n\n") + "\n\n".join(alert_messages), 
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer(_("You have no alerts set."), parse_mode=ParseMode.HTML)


@alerts_router.message(StateFilter(None), F.text == __("🔔 Add Alert"))
async def start_add_alert(message: Message, state: FSMContext):
    await message.answer(
        _("Which coin do you want to set an alert for? (e.g., BTC, ETH):"),
        reply_markup=get_popular_crypto_kb()
    )
    await state.set_state(CreateAlert.waiting_for_symbol)


@alerts_router.message(CreateAlert.waiting_for_symbol, F.text == __("❌ Cancel"))
async def cancel_add_alert(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(_("Alert creation cancelled."), reply_markup=main_menu())

@alerts_router.message(CreateAlert.waiting_for_symbol)
async def process_alert_symbol(message: Message, state: FSMContext, http_session:aiohttp.ClientSession):
    symbol = message.text.upper().strip()
    current_price = await get_crypto_price(symbol=symbol,http_session=http_session)
    if current_price:
        await state.update_data(symbol=symbol, current_price=current_price)
        await message.answer(
            _("Current price of <b>{symbol}</b> is ${current_price:,.2f}.\n"
            "At what price do you want to set the alert?").format(symbol=symbol, current_price=current_price),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )
        await state.set_state(CreateAlert.waiting_for_price)
    else:
        await message.answer(_("❌ Could not find <b>{symbol}</b>. Please try another symbol:").format(symbol=symbol),parse_mode=ParseMode.HTML)

@alerts_router.message(CreateAlert.waiting_for_price)
async def process_alert_price(message: Message, state: FSMContext, session: AsyncSession):
    try:
        target_price = float(message.text.strip().replace(',', '.'))
        data = await state.get_data()
        symbol = data.get("symbol")
        current_price = data.get("current_price")
        direction = "UP" if target_price > current_price else "DOWN"
        await add_alert(session=session,
            tg_id=message.from_user.id,
            symbol=symbol,
            target_price=target_price,
            direction=direction
        )
        emoji = "📈" if direction == "UP" else "📉"
        direction_text = _("Above") if direction == "UP" else _("Below")
        msg=_("Alert set: <b>{symbol}</b> {emoji}\n"
              "Target: <code>${target_price:,.2f}</code>\n"
              "(Trigger when price goes {direction})").format(
                  symbol=symbol, 
                  emoji=emoji, 
                  target_price=target_price, 
                  direction=direction_text
              )
        await message.answer(
            msg,
            reply_markup=main_menu(),
            parse_mode=ParseMode.HTML
        )
        await state.clear()
    except ValueError:
        await message.answer(_("❌ Please enter a valid number (e.g., 55000.50):"), parse_mode=ParseMode.HTML)


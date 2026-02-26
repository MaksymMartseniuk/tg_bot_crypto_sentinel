from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardRemove
from app.keyboards.builders import main_menu
from app.keyboards.price_kb import get_popular_crypto_kb
from app.services.binance_api import get_crypto_price
from app.database.requests import add_alert, get_user_alerts
alerts_router=Router()

class CreateAlert(StatesGroup):
    waiting_for_symbol=State()
    waiting_for_price=State()

@alerts_router.message(F.text == "🔔 Add Alert")
async def start_add_alert(message: Message, state: FSMContext):
    await message.answer(
        "Which coin do you want to set an alert for? (e.g., BTC, ETH):",
        reply_markup=get_popular_crypto_kb()
    )
    await state.set_state(CreateAlert.waiting_for_symbol)

@alerts_router.message(F.text=="📋 My Alerts")
async def show_user_alerts(message: Message):
    alerts_user = await get_user_alerts(message.from_user.id)
    if alerts_user:
        alert_messages = []
        for alert in alerts_user:
            emoji = "📈" if alert.direction == "UP" else "📉"
            status = "Active" if alert.is_active else "Triggered"
            alert_messages.append(
                f"{emoji} <b>{alert.symbol}</b> - Target: <code>${alert.target_price:,.2f}</code> - {status}"
            )
        await message.answer("\n".join(alert_messages), parse_mode=ParseMode.HTML)
    else:
        await message.answer("You have no alerts set.", parse_mode=ParseMode.HTML)

@alerts_router.message(CreateAlert.waiting_for_symbol, F.text == "❌ Cancel")
async def cancel_add_alert(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Alert creation cancelled.", reply_markup=main_menu())

@alerts_router.message(CreateAlert.waiting_for_symbol)
async def process_alert_symbol(message: Message, state: FSMContext):
    symbol = message.text.upper().strip()
    current_price = await get_crypto_price(symbol)
    if current_price:
        await state.update_data(symbol=symbol, current_price=current_price)
        await message.answer(
            f"Current price of <b>{symbol}</b> is ${current_price:.2f}.\n"
            "At what price do you want to set the alert?",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )
        await state.set_state(CreateAlert.waiting_for_price)
    else:
        await message.answer(f"❌ Could not find <b>{symbol}</b>. Please try another symbol:",parse_mode=ParseMode.HTML) #TODO:add keuboard

@alerts_router.message(CreateAlert.waiting_for_price)
async def process_alert_price(message: Message, state: FSMContext):
    try:
        target_price = float(message.text.strip().replace(',', '.'))
        data = await state.get_data()
        symbol = data.get("symbol")
        current_price = data.get("current_price")
        direction = "UP" if target_price > current_price else "DOWN"
        await add_alert(
            tg_id=message.from_user.id,
            symbol=symbol,
            target_price=target_price,
            direction=direction
        )
        emoji = "📈" if direction == "UP" else "📉"
        await message.answer(
            f"✅ Alert set: <b>{symbol}</b> {emoji}\n"
            f"Target: <code>${target_price:,.2f}</code>\n"
            f"(Trigger when price goes {'above' if direction == 'UP' else 'below'})",
            reply_markup=main_menu(),
            parse_mode=ParseMode.HTML
        )
        await state.clear()
    except ValueError:
        await message.answer("❌ Invalid price. Please enter a valid number:", parse_mode=ParseMode.HTML) #TODO:add keuboard


from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from app.keyboards.builders import main_menu
from app.keyboards.price_kb import get_popular_crypto_kb
from app.services.binance_api import get_crypto_price


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
            reply_markup=main_menu(),
            parse_mode=ParseMode.HTML
        )
        await state.set_state(CreateAlert.waiting_for_price)
    else:
        await message.answer(f"❌ Could not find <b>{symbol}</b>. Please try another symbol:")

@alerts_router.message(CreateAlert.waiting_for_price)
async def process_alert_price(message: Message, state: FSMContext):
    try:
        price = float(message.text.strip())
        data = await state.get_data()
        symbol = data.get("symbol")
        #TODO: Save the alert to the database here
        await message.answer(
            f"✅ Alert set for <b>{symbol}</b> at ${price:.2f}.\n"
            "You will be notified when the price reaches this level.",
            reply_markup=main_menu(),
            parse_mode=ParseMode.HTML
        )
        await state.clear()
    except ValueError:
        await message.answer("❌ Invalid price. Please enter a valid number:")


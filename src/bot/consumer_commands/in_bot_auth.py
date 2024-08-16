from aiogram import html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from sqlalchemy.exc import NoResultFound

from src.bot.main import dp
from src.database.facade import dao


class ConsumerAuthState(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


@dp.message(Command("auth"))
async def command_auth_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Enter {html.bold("Meduza")} account's username:")
    await state.set_state(ConsumerAuthState.waiting_for_username)


@dp.message(ConsumerAuthState.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    try:
        consumer = await dao.consumer.retrieve_where(username=message.text)
        await state.update_data(consumer_id=consumer.id, hashed_password=consumer.hashed_password)
        await state.set_state(ConsumerAuthState.waiting_for_password)
        await message.answer('Enter password:')
    except NoResultFound:
        await message.answer('Invalid username.')


@dp.message(ConsumerAuthState.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    def verify_password(stored_hash: str, pass_to_check: str) -> bool:
        return pass_to_check == stored_hash

    state_data = await state.get_data()

    consumer_id: int = state_data['consumer_id']
    hashed_password: str = state_data['hashed_password']

    password: str = message.text
    telegram_id: int = message.from_user.id

    if verify_password(
            stored_hash=hashed_password,
            pass_to_check=password
    ):
        await dao.consumer.update(consumer_id, current_id=telegram_id)
        await message.answer(
            f"{html.bold("New Telegram account authorized.")}\n"
            f"You can perform your actions \nby command /actions.")
    else:
        await message.answer(
            f"{html.bold("Invalid credentials.")}\n"
            f"Pass credentials again \nby command /auth.")

    await state.set_state(None)


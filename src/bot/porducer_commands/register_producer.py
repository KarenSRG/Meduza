from aiogram import html

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from src.bot.api_actions import init_producer_registration, confirm_producer_registration
from src.bot.main import dp

from src.database.facade import dao

from src.apps.producers.schemas import ProducerCreateSchema


class ProducerRegisterState(StatesGroup):
    waiting_for_contact = State()
    waiting_for_conf_code = State()


@dp.message(Command("register"))
async def command_register_handler(message: Message, state: FSMContext):
    button_phone = [KeyboardButton(text='Share phone number', request_contact=True)]
    keyboard = ReplyKeyboardMarkup(keyboard=[button_phone], resize_keyboard=True)

    await message.answer("Share your phone number.", reply_markup=keyboard)
    await state.set_state(ProducerRegisterState.waiting_for_contact)


@dp.message(lambda message: message.contact is not None)
async def handle_contact(message: Message, state: FSMContext):
    current_state = await state.get_state()
    telegram_id = message.from_user.id
    phone_number = message.contact.phone_number

    await message.delete()

    if current_state == "ProducerRegisterState:waiting_for_contact":
        await message.answer(

            f"Confirmation code sent, check \n"
            f"{html.bold("Telegram Notifications")}.\n"
            f"\nSign-in by {html.italic("meduzahandler8")}\n"
            "\nEncrypt confirmation code with this algorithm (case doesn't matter):\n" +
            html.bold("\nA - 1    B - 2    C - 3    D - 4    E - 5"
                      "\nF - 6    G - 7    H - 8    I - 9    J - 0")
        )

        await init_producer_registration(phone_number, telegram_id)
        await state.update_data(phone_number=phone_number)
        await state.set_state(ProducerRegisterState.waiting_for_conf_code)


def parse_conf_code(conf_code: str) -> str:
    letter_list = ["J", "A", "B", "C", "D", "E", "F", "G", "H", "I"]
    result = ""

    for letter in conf_code.upper():
        if letter not in letter_list:
            return "invalid conf code"
        result += str(letter_list.index(letter))
    return result


@dp.message(ProducerRegisterState.waiting_for_conf_code)
async def process_conf_code(message: Message, state: FSMContext):
    conf_code = parse_conf_code(message.text)

    sender = message.from_user
    telegram_id = sender.id
    phone_number = (await state.get_data())["phone_number"]

    if conf_code.isnumeric():
        result = await confirm_producer_registration(conf_code, telegram_id)
        if result["status"] == "success":

            if sender is not None:
                verbose_name = sender.username if sender else sender.first_name
            else:
                verbose_name = 'Unknown'

            new_producer = ProducerCreateSchema(
                id=telegram_id,
                username=verbose_name,
                phone_number=phone_number,
                session_string=result["session"]
            )

            await dao.producer.create(**new_producer.dict())
        await message.answer(result["status"])
    else:
        await message.answer(f"Confirmation code is {html.bold("invalid")}, try again.")

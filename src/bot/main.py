import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.exc import NoResultFound

from src.bot.config import BOT_TOKEN

from src.bot.consumer_commands.filtration_actions import command_fromuser, command_contains, command_startswith
from src.bot.consumer_commands.filtration_actions import command_actions, command_fromchat

from src.bot.consumer_commands.in_bot_auth import ConsumerAuthState, process_username
from src.bot.consumer_commands.in_bot_auth import command_auth, process_password

from src.bot.porducer_commands.register_producer import command_register, handle_prod_contact
from src.bot.porducer_commands.register_producer import process_conf_code, ProducerRegisterState

from src.database.facade import dao

dp = Dispatcher()

# # Registration of Consumer - Related commands. # #

# Message filtration actions.
dp.message.register(command_actions, Command("actions"))
dp.message.register(command_startswith, Command("startswith"))
dp.message.register(command_contains, Command("contains"))
dp.message.register(command_fromuser, Command("fromuser"))
dp.message.register(command_fromchat, Command("fromchat"))

# Consumer authentication
dp.message.register(command_auth, Command("auth"))
dp.message.register(process_username, ConsumerAuthState.waiting_for_username)
dp.message.register(process_password, ConsumerAuthState.waiting_for_username)
dp.message.register(command_startswith, Command("startswith"))
dp.message.register(command_contains, Command("contains"))

# # Registration of Producer - Related commands. # #

# Registration of Producer.
dp.message.register(command_register, Command("register"))
dp.message.register(handle_prod_contact, lambda message: message.contact is not None)
dp.message.register(process_conf_code, ProducerRegisterState.waiting_for_conf_code)


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    current_user_id: int = message.from_user.id
    try:  # Get producer with this ID
        await dao.producer.retrieve(current_user_id)
        await message.answer(f"{html.bold(message.from_user.full_name)}, you are producer.")
    except NoResultFound:
        try:  # If there are no producer with this ID, check this ID in consumers
            await dao.consumer.retrieve_where(current_id=current_user_id)
            await message.answer(f"{html.bold(message.from_user.full_name)}, welcome type /actions for info.")
        except NoResultFound:  # Finally, if current user not in system, suggest registration.
            await message.answer(
                f"{html.bold("You are unauthorized.")}\n"
                f"{html.bold('1.')} If you has account, pass credentials by command /auth.\n"
                f"{html.bold('2.')} If you want to be producer use command /register.")

    await state.set_state(None)


async def run_controller_bot() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

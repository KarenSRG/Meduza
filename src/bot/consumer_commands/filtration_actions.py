from aiogram.filters import Command
from aiogram.types import Message

from src.bot.main import dp
from aiogram import html


@dp.message(Command("actions"))
async def command_actions(message: Message) -> None:
    actions = (
        (f"  /startswith {html.italic("query")}", f"Get messages, which started with {html.italic("query")}."),
        (f"  /contains {html.italic("query")}", f"Get messages, which contains {html.italic("query")}."),
        (f"  /fromchat {html.italic("query")}", f"Get messages from certain {html.italic("query")} chat."),
        (f"  /fromuser {html.italic("query")}", f"Get messages from certain {html.italic("query")} user.")
    )

    await message.answer(f"This is action-list that you can use: \n\n\n" +
                         "\n\n".join([f"{action[0]}  ->  {action[1]}" for action in actions]))



@dp.message(Command("startswith"))
async def command_startswith(message: Message) -> None:
    pass


@dp.message(Command("contains"))
async def command_contains(message: Message) -> None:
    pass


@dp.message(Command("fromchat"))
async def command_fromchat(message: Message) -> None:
    pass


@dp.message(Command("fromuser"))
async def command_fromuser(message: Message) -> None:
    pass

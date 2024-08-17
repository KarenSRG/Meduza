from typing import Awaitable

from aiogram.types import Message

from aiogram import html

from src.database.facade import dao
from src.permissions import is_active_producer


async def command_actions(message: Message) -> None:
    actions = (
        (f"  /startswith {html.italic("query")}", f"Get messages, which started with {html.italic("query")}."),
        (f"  /contains {html.italic("query")}", f"Get messages, which contains {html.italic("query")}."),
        (f"  /fromchat {html.italic("query")}", f"Get messages from certain {html.italic("query")} chat."),
        (f"  /fromuser {html.italic("query")}", f"Get messages from certain {html.italic("query")} user.")
    )

    await message.answer(f"This is action-list that you can use: \n\n\n" +
                         "\n\n".join([f"{action[0]}  ->  {action[1]}" for action in actions]))


async def long_answer(message: Message, text: str) -> None:
    if len(text) > 4096:
        parts = [text[i:i + 4096] for i in range(0, len(text), 4096)]
        for part in parts:
            await message.answer(part)
    else:
        await message.answer(text)


async def query_parser(message: Message) -> str or Awaitable:
    if await is_active_producer(message.from_user.id):
        text = message.text.split()
        if len(text) > 2:
            return message.text[message.text.index(" "):].strip()
        return message.answer(f"Invalid {html.bold('query')}.")
    return message.answer(f"This {html.bold('command')} not allowed for you.")


async def command_startswith(message: Message) -> None:
    result = await query_parser(message)
    if type(result) is str:
        message_list = await dao.message.startswith(result)
        if message_list:
            answer_template = f"Messages starting starting with {html.bold(result)}:\n\n\n" + \
                              "\n".join(message.text for message in message_list)
            await long_answer(message, answer_template)
        else:
            await message.answer(f"There are not messages starting with {html.bold(result)}.")
    else:
        await result


async def command_contains(message: Message) -> None:
    result = await query_parser(message)
    if type(result) is str:
        message_list = await dao.message.contains(result)
        if message_list:
            answer_template = f"Messages, that contains {html.bold(result)}:\n\n\n" + \
                              "\n".join(message.text for message in message_list)
            await long_answer(message, answer_template)
        else:
            await message.answer(f"There are not messages, that contains {html.bold(result)}.")
    else:
        await result


async def command_fromchat(message: Message) -> None:
    result = await query_parser(message)
    if type(result) is str:
        message_list = await dao.message.fromchat(result)
        if message_list:
            answer_template = f"Messages from chat {html.bold(result)}:\n\n\n" + \
                              "\n".join(message.text for message in message_list)
            await long_answer(message, answer_template)
        else:
            await message.answer(f"There are not messages from {html.bold(result)}.")
    else:
        await result


async def command_fromuser(message: Message) -> None:
    result = await query_parser(message)
    if type(result) is str:
        message_list = await dao.message.fromuser(result)
        if message_list:
            answer_template = f"Messages from user {html.bold(result)}:\n\n\n" + \
                              "\n".join(message.text for message in message_list)
            await long_answer(message, answer_template)
        else:
            await message.answer(f"There are not messages from {html.bold(result)}.")
    else:
        await result

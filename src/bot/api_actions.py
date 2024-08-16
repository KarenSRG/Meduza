import asyncio
import json
import logging
import os

from sqlalchemy.exc import NoResultFound
from telethon import TelegramClient, events
from telethon.errors import RPCError, SessionPasswordNeededError, rpcerrorlist, AuthKeyUnregisteredError
from telethon.sessions import StringSession

from src.bot.config import API_ID, API_HASH
from src.apps.producers.models import Producer
from src.database.facade import dao

from src.apps.messages.schemas import MessageCreateSchema
from src.apps.chats.schemas import ChatCreateSchema


async def init_producer_registration(phone_number: str, telegram_id: int):
    client = TelegramClient(StringSession(), API_ID, API_HASH)

    await client.connect()

    conf_code = await client.send_code_request(phone_number)
    session_string = client.session.save()

    await client.disconnect()

    with open(os.path.abspath("bot/pending_sessions.json"), 'r+') as file:
        data = json.load(file)

        for ses in data["reg_sessions"]:
            if ses["phone_number"] == phone_number:
                data["reg_sessions"].remove(ses)

        new_ses_registration = {
            "phone_number": phone_number,
            "telegram_id": telegram_id,
            "conf_code_hash": conf_code.phone_code_hash,
            "session": session_string
        }

        data["reg_sessions"].append(new_ses_registration)

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


async def confirm_producer_registration(conf_code: str, telegram_id: int) -> dict:
    with open(os.path.abspath("bot/pending_sessions.json"), 'r+') as file:
        data = json.load(file)

        for ses in data["reg_sessions"]:
            if ses["telegram_id"] == telegram_id:
                session = StringSession(ses["session"])
                client = TelegramClient(session, API_ID, API_HASH)

                await client.connect()
                if await client.is_user_authorized():
                    return {"status": "Authorized already."}
                try:
                    await client.sign_in(ses["phone_number"], conf_code, phone_code_hash=ses["conf_code_hash"])
                    data["reg_sessions"].remove(ses)
                except SessionPasswordNeededError:
                    return {"status": "Need to put password."}
                except RPCError as e:
                    return {"status": f"Failed to sign in: {e}"}
                finally:
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    await client.disconnect()
                return {"status": "success", "session": ses["session"]}
    return {"status": "Producer registration session\nnot found, try /register again."}


async def start_monitoring_for(producer: Producer):
    client = TelegramClient(StringSession(producer.session_string), API_ID, API_HASH)
    await client.connect()

    @client.on(events.NewMessage())
    async def handler(event):
        try:
            chat = await event.get_chat()
            chat_id = chat.id
            chat_name = chat.title if hasattr(chat, 'title') else 'Private Chat'
        except rpcerrorlist.ChannelPrivateError:
            return

        try:
            await dao.chat.retrieve(chat_id)
        except NoResultFound:
            new_chat = ChatCreateSchema(id=chat_id, chat_title=chat_name, producer_id=producer.id)
            await dao.chat.create(**new_chat.dict())

        # Process the messages
        sender = await event.get_sender()
        if sender is not None:
            sender_username = sender.username if sender else sender.first_name
        else:
            sender_username = 'unknown'
        try:
            sender_bot = sender.bot
        except AttributeError:
            sender_bot = True

        if not sender_bot and sender_username is not None:
            message_text = event.text.replace('\n', '') if event.text else ''
            if message_text:
                logging.info(f"[{sender_username}][{chat_name}]: {message_text}")

                new_message = MessageCreateSchema(
                    text=message_text,
                    chat_id=chat_id,
                    chat_title=chat_name,
                    producer_id=producer.id,
                    sender_user_id=sender.id if sender else None,
                    sender_username=sender_username
                )

                await dao.message.create(**new_message.dict())

                # triggered_events = await self.compare_events_and_message(message_data)

    await client.run_until_disconnected()


async def run_monitoring_bot():
    current_producers = []
    while True:
        for producer in await dao.producer.list():
            if producer not in current_producers:
                current_producers.append(producer)
                try:
                    await asyncio.create_task(start_monitoring_for(producer))
                except AuthKeyUnregisteredError:
                    await dao.producer.update(obj_id=producer.id, active=False)
        await asyncio.sleep(10)


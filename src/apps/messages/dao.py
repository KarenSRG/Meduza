from typing import Any

from sqlalchemy import select

from src.apps.messages.models import Message
from src.database.crud import AsyncCRUD
from src.database.session_decorator import db_session


class MessageDAO(AsyncCRUD):
    def __init__(self):
        super().__init__(Message)

    @db_session
    async def startswith(self, session, value) -> list[dict[str, Any]]:
        query = select(self.model).where(self.model.text.startswith(value))
        result = await session.execute(query)
        return result.scalars().all()

    @db_session
    async def contains(self, session, value) -> list[dict[str, Any]]:
        query = select(self.model).where(self.model.text.contains(value))
        result = await session.execute(query)
        return result.scalars().all()

    @db_session
    async def fromchat(self, session, chat) -> list[dict[str, Any]]:
        query = select(self.model).where(self.model.chat_title == chat)
        result = await session.execute(query)
        return result.scalars().all()

    @db_session
    async def fromuser(self, session, username) -> list[dict[str, Any]]:
        query = select(self.model).where(self.model.sender_username == username)
        result = await session.execute(query)
        return result.scalars().all()

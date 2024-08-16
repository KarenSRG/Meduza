
from typing import Any

from sqlalchemy import select

from src.apps.consumers.models import Consumer
from src.database.crud import AsyncCRUD
from src.database.session_decorator import db_session


class ConsumerDAO(AsyncCRUD):
    def __init__(self):
        super().__init__(Consumer)

    @db_session
    async def retrieve_where(self, session, **kwargs) -> dict[str, Any]:
        query = select(self.model)
        for attr, value in kwargs.items():
            query = query.where(getattr(self.model, attr) == value)
        result = await session.execute(query)
        return result.scalar_one()

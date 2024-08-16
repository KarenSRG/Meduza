from typing import Any

from sqlalchemy.future import select

from src.database.session_decorator import db_session


# TODO handle noresultfound in chat retrieve
# asyncpg.exceptions.UniqueViolationError: duplicate key value violates unique constraint "chats_pkey"
# DETAIL:  Key (id)=(1966291562) already exists.

# noinspection PyTypeChecker
class AsyncCRUD:
    def __init__(self, model):
        self.model = model

    @db_session
    async def create(self, session, **kwargs):
        instance = self.model(**kwargs)
        session.add(instance)
        await session.commit()
        return instance

    @db_session
    async def retrieve(self, session, obj_id) -> dict[str, Any]:
        query = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(query)
        return result.scalar_one()

    @db_session
    async def list(self, session) -> list[dict[str, Any]]:
        query = select(self.model)
        result = await session.execute(query)
        return result.scalars().all()

    @db_session
    async def update(self, session, obj_id, **kwargs):
        query = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(query)
        instance = result.scalar_one()

        for attr, value in kwargs.items():
            setattr(instance, attr, value)

        await session.commit()
        return instance

    @db_session
    async def delete(self, session, obj_id) -> None:
        query = select(self.model).where(self.model.id == obj_id)
        result = await session.execute(query)
        instance = result.scalar_one()
        await session.delete(instance)
        await session.commit()

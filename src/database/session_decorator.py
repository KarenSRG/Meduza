from functools import wraps
from src.database.engine import async_session
from sqlalchemy.exc import SQLAlchemyError


def db_session(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with async_session() as session:
            async with session.begin():
                try:
                    return await func(self, session, *args, **kwargs)
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
    return wrapper


from sqlalchemy.exc import NoResultFound

from src.database.facade import dao


async def is_active_producer(telegram_id: int) -> bool:
    try:
        return (await dao.producer.retrieve(telegram_id)).active
    except NoResultFound:
        return True

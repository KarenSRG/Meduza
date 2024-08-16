from fastapi import HTTPException, status, APIRouter
from sqlalchemy import exc

from src.apps.producers.schemas import ProducerModel
from src.database.facade import dao

router = APIRouter()


@router.get("/producers/", status_code=status.HTTP_200_OK)
async def list_producers():
    try:
        return await dao.producer.list()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/producer/", response_model=ProducerModel,status_code=status.HTTP_200_OK)
async def retrieve_producer(telegram_id: int):
    try:
        return await dao.producer.retrieve(telegram_id)
    except exc.NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

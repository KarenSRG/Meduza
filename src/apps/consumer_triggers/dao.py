from src.apps.producers.models import Producer
from src.database.crud import AsyncCRUD


class ProducerDAO(AsyncCRUD):
    def __init__(self):
        super().__init__(Producer)

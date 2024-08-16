from src.apps.messages.models import Message
from src.database.crud import AsyncCRUD


class MessageDAO(AsyncCRUD):
    def __init__(self):
        super().__init__(Message)

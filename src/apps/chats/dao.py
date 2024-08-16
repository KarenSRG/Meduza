from src.apps.chats.models import Chat
from src.database.crud import AsyncCRUD


class ChatDAO(AsyncCRUD):
    def __init__(self):
        super().__init__(Chat)

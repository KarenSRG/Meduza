from datetime import datetime
from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: int
    text: str
    timestamp: datetime
    chat_id: int
    chat_title: str
    producer_id: int


class MessageCreateSchema(BaseModel):

    text: str
    chat_id: int
    chat_title: str
    producer_id: int
    sender_user_id: int
    sender_username: str

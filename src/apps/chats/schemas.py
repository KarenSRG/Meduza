from pydantic import BaseModel


class ChatModel(BaseModel):
    id: int
    chat_title: str
    producer_id: int

    class Config:
        from_attributes = True


class ChatCreateSchema(BaseModel):
    id: int
    chat_title: str
    producer_id: int

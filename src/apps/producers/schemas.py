from datetime import datetime

from pydantic import BaseModel


class ProducerModel(BaseModel):
    id: int
    username: str
    created_at: datetime
    active: bool
    session_string: str


class ProducerCreateSchema(BaseModel):
    id: int
    username: str
    phone_number: str
    session_string: str


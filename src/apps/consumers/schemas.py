from datetime import datetime

from pydantic import BaseModel


class ConsumerModel(BaseModel):
    id: int
    username: str
    created_at: datetime
    active: bool
    session_string: str




from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database.engine import Base


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    text: Mapped[str] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("chats.id"))
    chat_title: Mapped[str] = mapped_column()
    producer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("producers.id"))

    sender_user_id: Mapped[int] = mapped_column(BigInteger)
    sender_username: Mapped[str] = mapped_column()

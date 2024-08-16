from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.database.engine import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    chat_title: Mapped[str] = mapped_column(nullable=True)
    producer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("producers.id"))



from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database.engine import Base


class Producer(Base):
    __tablename__ = "producers"
    id: Mapped[int] = mapped_column(BigInteger, index=True, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()

    # proxy_id: Mapped[int] = mapped_column(ForeignKey('proxy.id'))

    session_string: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

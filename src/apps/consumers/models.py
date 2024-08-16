from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database.engine import Base


class Consumer(Base):
    __tablename__ = "consumers"
    id: Mapped[int] = mapped_column(index=True, primary_key=True, autoincrement=True, unique=True)

    current_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()

    active: Mapped[bool] = mapped_column(default=True)

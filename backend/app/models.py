from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))


class Principle(Base):
    __tablename__ = "principles"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(8), unique=True)
    source: Mapped[str] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(String(60))
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text)
    example: Mapped[str] = mapped_column(Text)

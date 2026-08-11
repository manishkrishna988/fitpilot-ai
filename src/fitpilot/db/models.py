from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from fitpilot.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    height_cm: Mapped[float] = mapped_column(Float)
    weight_kg: Mapped[float] = mapped_column(Float)
    goal: Mapped[str] = mapped_column(String(50))
    experience_level: Mapped[str] = mapped_column(String(50))
    training_days_per_week: Mapped[int] = mapped_column(Integer)

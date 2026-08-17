from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fitpilot.db.base import Base

user_equipment = Table(
    "user_equipment",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("equipment_id", ForeignKey("equipment.id"), primary_key=True),
)


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    users: Mapped[list["User"]] = relationship(
        secondary=user_equipment,
        back_populates="available_equipment",
    )


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
    available_equipment: Mapped[list[Equipment]] = relationship(
        secondary=user_equipment,
        back_populates="users",
    )

    exercise_limitations: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
    )

from datetime import date

from sqlalchemy import JSON, Column, Date, Float, ForeignKey, Integer, String, Table
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

    workout_plans: Mapped[list["WorkoutPlan"]] = relationship(
        back_populates="user",
    )


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    week_start_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50), default="active")

    user: Mapped["User"] = relationship(
        back_populates="workout_plans",
    )
    workout_days: Mapped[list["WorkoutDay"]] = relationship(
        back_populates="workout_plan",
    )


class WorkoutDay(Base):
    __tablename__ = "workout_days"

    id: Mapped[int] = mapped_column(primary_key=True)
    workout_plan_id: Mapped[int] = mapped_column(ForeignKey("workout_plans.id"))
    day_number: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(100))

    workout_plan: Mapped["WorkoutPlan"] = relationship(
        back_populates="workout_days",
    )

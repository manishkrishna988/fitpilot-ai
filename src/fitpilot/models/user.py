from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class FitnessGoal(StrEnum):
    FAT_LOSS = "fat_loss"
    STRENGTH = "strength"
    MUSCLE_GAIN = "muscle_gain"
    FAT_LOSS_AND_STRENGTH = "fat_loss_and_strength"


class ExperienceLevel(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"


class UserProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=18, le=100)
    height_cm: float = Field(gt=0, le=250)
    weight_kg: float = Field(gt=0, le=400)
    goal: FitnessGoal
    experience_level: ExperienceLevel
    training_days_per_week: int = Field(ge=1, le=7)
    available_equipment: list[str] = Field(default_factory=list)
    exercise_limitations: list[str] = Field(default_factory=list)


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    height_cm: float
    weight_kg: float
    goal: FitnessGoal
    experience_level: ExperienceLevel
    training_days_per_week: int

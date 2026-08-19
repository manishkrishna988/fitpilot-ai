from datetime import date

from pydantic import BaseModel, ConfigDict


class WorkoutPlanCreate(BaseModel):
    user_id: int
    week_start_date: date


class WorkoutPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    week_start_date: date
    status: str

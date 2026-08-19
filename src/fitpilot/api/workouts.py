from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fitpilot.db.models import User, WorkoutDay, WorkoutPlan
from fitpilot.db.session import get_db
from fitpilot.models.workout import WorkoutPlanCreate, WorkoutPlanResponse
from fitpilot.services.workout_templates import WORKOUT_TEMPLATES

router = APIRouter(prefix="/workout-plans", tags=["Workout Plans"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=WorkoutPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workout_plan(
    plan: WorkoutPlanCreate,
    db: DatabaseSession,
) -> WorkoutPlan:
    user = db.get(User, plan.user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    workout_plan = WorkoutPlan(
        user_id=plan.user_id,
        week_start_date=plan.week_start_date,
    )

    template = WORKOUT_TEMPLATES.get(user.training_days_per_week)

    if template is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No workout template available for this training frequency",
        )

    for day_number, day_name in enumerate(template, start=1):
        workout_plan.workout_days.append(
            WorkoutDay(
                day_number=day_number,
                name=day_name,
            )
        )

    db.add(workout_plan)
    db.commit()
    db.refresh(workout_plan)

    return workout_plan

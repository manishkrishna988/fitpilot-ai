from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fitpilot.db.models import PlannedExercise, User, WorkoutDay, WorkoutPlan
from fitpilot.db.session import get_db
from fitpilot.models.workout import WorkoutPlanCreate, WorkoutPlanResponse
from fitpilot.services.workout_templates import (
    EXERCISE_SUBSTITUTIONS,
    EXERCISE_TEMPLATES,
    WORKOUT_TEMPLATES,
)

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

    available_equipment = {equipment.name for equipment in user.available_equipment}

    for day_number, day_name in enumerate(template, start=1):
        workout_day = WorkoutDay(
            day_number=day_number,
            name=day_name,
        )

        exercise_template = EXERCISE_TEMPLATES.get(day_name, [])

        for (
            exercise_name,
            target_sets,
            target_reps,
            required_equipment,
        ) in exercise_template:
            if required_equipment not in available_equipment:
                substitution = EXERCISE_SUBSTITUTIONS.get(exercise_name)

                if substitution is None:
                    continue

                (
                    exercise_name,
                    target_sets,
                    target_reps,
                    required_equipment,
                ) = substitution

                if required_equipment not in available_equipment:
                    continue

            workout_day.planned_exercises.append(
                PlannedExercise(
                    name=exercise_name,
                    target_sets=target_sets,
                    target_reps=target_reps,
                )
            )

        workout_plan.workout_days.append(workout_day)

    db.add(workout_plan)
    db.commit()
    db.refresh(workout_plan)

    return workout_plan

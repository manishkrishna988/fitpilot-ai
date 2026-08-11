from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fitpilot.db.models import User
from fitpilot.db.session import get_db
from fitpilot.models.user import UserProfileCreate, UserProfileResponse

router = APIRouter(prefix="/users", tags=["Users"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/profile",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_profile(
    profile: UserProfileCreate,
    db: DatabaseSession,
) -> User:
    """Validate and persist a new user profile."""

    user = User(
        name=profile.name,
        age=profile.age,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        goal=profile.goal.value,
        experience_level=profile.experience_level.value,
        training_days_per_week=profile.training_days_per_week,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get(
    "/{user_id}",
    response_model=UserProfileResponse,
)
def get_user_profile(
    user_id: int,
    db: DatabaseSession,
) -> User:
    """Return a stored user profile by ID."""

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user

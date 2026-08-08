from fastapi import APIRouter, status

from fitpilot.models.user import UserProfileCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/profile", status_code=status.HTTP_201_CREATED)
def create_user_profile(profile: UserProfileCreate) -> UserProfileCreate:
    """Validate and return a newly created user profile."""
    return profile

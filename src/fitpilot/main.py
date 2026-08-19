from fastapi import FastAPI

from fitpilot.api.health import router as health_router
from fitpilot.api.users import router as users_router
from fitpilot.api.workouts import router as workouts_router


def create_app() -> FastAPI:
    """Create and configure the FitPilot FastAPI application."""
    app = FastAPI(
        title="FitPilot AI API",
        description=(
            "API for personalised fitness planning, workout tracking, "
            "progress analysis, and controlled plan adaptation."
        ),
        version="0.1.0",
    )

    app.include_router(health_router)
    app.include_router(users_router)
    app.include_router(workouts_router)

    return app


app = create_app()

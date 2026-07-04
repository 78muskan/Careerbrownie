from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401 - imported so SQLAlchemy registers all models.
from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router
from app.api.routes.chatbot import router as chatbot_router
from app.api.routes.counsellors import router as counsellors_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.roadmaps import router as roadmaps_router
from app.api.routes.sessions import router as sessions_router
from app.api.routes.students import router as students_router
from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Backend API for Career Brownie AI career counselling platform.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
    app.include_router(students_router, prefix=settings.API_V1_PREFIX)
    app.include_router(counsellors_router, prefix=settings.API_V1_PREFIX)
    app.include_router(sessions_router, prefix=settings.API_V1_PREFIX)
    app.include_router(chatbot_router, prefix=settings.API_V1_PREFIX)
    app.include_router(recommendations_router, prefix=settings.API_V1_PREFIX)
    app.include_router(roadmaps_router, prefix=settings.API_V1_PREFIX)
    app.include_router(admin_router, prefix=settings.API_V1_PREFIX)

    @app.get("/")
    def root():
        return {
            "message": "Welcome to Career Brownie Backend",
            "docs": "/docs",
            "health": "/health",
        }

    @app.get("/health")
    def health_check():
        return {
            "status": "ok",
            "service": "backend",
            "environment": settings.ENVIRONMENT,
        }

    return app


app = create_app()

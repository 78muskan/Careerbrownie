from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router
from app.api.routes.chatbot import router as chatbot_router
from app.api.routes.counsellors import router as counsellors_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.students import router as students_router

__all__ = [
    "admin_router",
    "auth_router",
    "chatbot_router",
    "counsellors_router",
    "recommendations_router",
    "students_router",
]

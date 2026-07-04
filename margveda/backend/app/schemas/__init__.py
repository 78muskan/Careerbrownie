from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, Token, UserResponse
from app.schemas.chatbot import ChatMessageRequest, ChatMessageResponse
from app.schemas.counsellor import (
    CounsellorDashboardResponse,
    CounsellorProfileResponse,
    CounsellorProfileUpdate,
)
from app.schemas.recommendation import (
    CareerRecommendationRequest,
    CareerRecommendationResponse,
    CollegePredictionRequest,
    CollegePredictionResponse,
    RoadmapRequest,
    RoadmapResponse,
    SavedRoadmapResponse,
    SkillGapRequest,
    SkillGapResponse,
)
from app.schemas.session import SessionCreate, SessionResponse, SessionStatusUpdate
from app.schemas.student import (
    SessionBookingRequest,
    StudentDashboardResponse,
    StudentProfileResponse,
    StudentProfileUpdate,
)

__all__ = [
    "AuthResponse",
    "CareerRecommendationRequest",
    "CareerRecommendationResponse",
    "ChatMessageRequest",
    "ChatMessageResponse",
    "CollegePredictionRequest",
    "CollegePredictionResponse",
    "CounsellorDashboardResponse",
    "CounsellorProfileResponse",
    "CounsellorProfileUpdate",
    "LoginRequest",
    "RegisterRequest",
    "RoadmapRequest",
    "RoadmapResponse",
    "SavedRoadmapResponse",
    "SessionBookingRequest",
    "SessionCreate",
    "SessionResponse",
    "SessionStatusUpdate",
    "SkillGapRequest",
    "SkillGapResponse",
    "StudentDashboardResponse",
    "StudentProfileResponse",
    "StudentProfileUpdate",
    "Token",
    "UserResponse",
]

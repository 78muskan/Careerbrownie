from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.counsellor import CounsellorProfile
from app.models.student import StudentProfile
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def register_user(self, payload: RegisterRequest) -> User:
        existing_user = self.get_user_by_email(payload.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        user = User(
            full_name=payload.full_name,
            email=payload.email,
            hashed_password=get_password_hash(payload.password),
            role=payload.role.value,
        )
        self.db.add(user)
        self.db.flush()

        if user.role == "student":
            self.db.add(StudentProfile(user_id=user.id))
        elif user.role == "counsellor":
            self.db.add(CounsellorProfile(user_id=user.id))

        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, payload: LoginRequest) -> User | None:
        user = self.get_user_by_email(payload.email)
        if user is None:
            return None

        if not verify_password(payload.password, user.hashed_password):
            return None

        return user

    def build_auth_response(self, user: User) -> AuthResponse:
        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role},
        )
        return AuthResponse(access_token=access_token, user=user)

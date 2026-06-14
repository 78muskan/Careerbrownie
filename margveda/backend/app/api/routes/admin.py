from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_roles
from app.models.user import User
from app.schemas.auth import UserResponse
from app.services.admin_service import AdminService


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
def get_admin_dashboard(
    _: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    return AdminService(db).dashboard()


@router.get("/users", response_model=list[UserResponse])
def list_users(
    _: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    return AdminService(db).list_users()


@router.patch("/users/{user_id}/active", response_model=UserResponse)
def set_user_active(
    user_id: int,
    is_active: bool = Body(embed=True),
    _: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    user = AdminService(db).set_user_active(user_id, is_active)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

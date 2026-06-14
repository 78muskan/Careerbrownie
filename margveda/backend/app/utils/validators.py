from fastapi import HTTPException, status


def ensure_owner_or_admin(owner_id: int, current_user_id: int, current_user_role: str) -> None:
    if current_user_role == "admin":
        return
    if owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own records",
        )

from fastapi import APIRouter, Depends, HTTPException
from ..models.user import User
from ..utils.db import db
from .auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = db.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

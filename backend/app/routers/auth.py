from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from ..models.user import User
from ..utils.db import db
from ..utils.auth import verify_password, get_password_hash, create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    avatar_url: str | None = None
    bio: str | None = None


@router.post("/signup")
def signup(user: UserCreate):
    # simple check unique username/email
    for u in db.users.values():
        if u.username == user.username or u.email == user.email:
            raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(
        id=0,
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password),
        avatar_url=user.avatar_url,
        bio=user.bio,
        posts=[],
    )
    db.add_user(new_user)
    return {"message": "User created"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in db.users.values() if u.username == form_data.username), None)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    user = db.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

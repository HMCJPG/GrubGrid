from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    password_hash: str
    avatar_url: str | None = None
    bio: str | None = None
    created_at: datetime = datetime.utcnow()
    posts: List[int] = []  # list of post ids

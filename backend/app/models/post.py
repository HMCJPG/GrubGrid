from datetime import datetime
from typing import List
from pydantic import BaseModel

class Post(BaseModel):
    id: int
    user_id: int
    image_url: str
    caption: str
    created_at: datetime = datetime.utcnow()
    likes: List[int] = []  # user ids
    comments: List[int] = []  # comment ids

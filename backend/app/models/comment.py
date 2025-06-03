from datetime import datetime
from pydantic import BaseModel

class Comment(BaseModel):
    id: int
    user_id: int
    post_id: int
    text: str
    created_at: datetime = datetime.utcnow()

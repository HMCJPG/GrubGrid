from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models.comment import Comment
from ..models.user import User
from ..models.post import Post
from ..utils.db import db
from .auth import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])

class CommentCreate(BaseModel):
    post_id: int
    text: str


@router.post("/", response_model=Comment)
def create_comment(comment: CommentCreate, current_user: User = Depends(get_current_user)):
    post = db.posts.get(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    new_comment = Comment(
        id=0,
        user_id=current_user.id,
        post_id=comment.post_id,
        text=comment.text,
    )
    db.add_comment(new_comment)
    post.comments.append(new_comment.id)
    return new_comment


@router.get("/post/{post_id}")
def get_comments(post_id: int):
    post = db.posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return [db.comments[cid] for cid in post.comments]

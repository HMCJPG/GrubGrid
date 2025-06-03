from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from ..models.post import Post
from ..models.user import User
from ..utils.db import db
from .auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/posts", tags=["posts"])

class PostCreate(BaseModel):
    caption: str
    image_url: str  # In real app, handle upload


@router.post("/", response_model=Post)
def create_post(post: PostCreate, current_user: User = Depends(get_current_user)):
    new_post = Post(
        id=0,
        user_id=current_user.id,
        image_url=post.image_url,
        caption=post.caption,
        likes=[],
        comments=[],
    )
    db.add_post(new_post)
    current_user.posts.append(new_post.id)
    return new_post


@router.get("/feed", response_model=List[Post])
def feed(skip: int = 0, limit: int = 20):
    posts = list(db.posts.values())
    posts.sort(key=lambda x: x.created_at, reverse=True)
    return posts[skip : skip + limit]


@router.post("/{post_id}/like")
def like_post(post_id: int, current_user: User = Depends(get_current_user)):
    post = db.posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if current_user.id not in post.likes:
        post.likes.append(current_user.id)
    return {"likes": len(post.likes)}

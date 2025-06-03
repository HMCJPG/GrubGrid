from fastapi import FastAPI
from .routers import auth, posts, comments, users

app = FastAPI(title="GrubGrid")

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Welcome to GrubGrid API"}

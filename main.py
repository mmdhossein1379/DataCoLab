from fastapi import FastAPI
from database import create_db_and_tables
from models import User, Post, Comment
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from crud import create_post, get_posts, get_post_by_id, update_post, delete_post, create_comment, get_comments_for_post
from database import get_session
from typing import Optional
from routes import posts, comments, users
from auth import router as auth_router
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("create successfully!")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(users.router, prefix="/users", tags=["Users"])


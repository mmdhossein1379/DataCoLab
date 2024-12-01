from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


# Users table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    email: str = Field(unique=True, max_length=100)
    password: str
    role: str = Field(default="Reader", max_length=20)  # role: Admin, Author, Reader
    created_at: Optional[str] = Field(default=None)
    name: str = Field(max_length=200)
    last_name: str = Field(max_length=200)
    posts: List["Post"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(back_populates="author")


# Posts table
class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    content: str
    tags: str = Field(max_length=255)  # format with ,
    author_id: int = Field(foreign_key="user.id")
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)

    author: "User" = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship(back_populates="post")


# Comment table
class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    post_id: int = Field(foreign_key="post.id")
    author_id: int = Field(foreign_key="user.id")
    created_at: Optional[str] = Field(default=None)

    post: "Post" = Relationship(back_populates="comments")
    author: "User" = Relationship(back_populates="comments")

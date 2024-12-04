from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_user, check_role
from models import Post
from database import get_session
from crud import create_post, get_all_posts, get_post_by_id, update_post, delete_post

router = APIRouter()


@router.post("/")
def create_new_post(title: str, content: str, tags: str, session: Session = Depends(get_session),
                    user=Depends(get_current_user)):
    check_role(user, ["Admin", "Author"])
    new_post = Post(title=title, content=content, tags=tags, author_id=user.id, created_at=datetime.utcnow())
    created_post = create_post(session, new_post)
    return {"message": "Post created successfully", "post": created_post}


@router.get("/")
def get_posts(page: int, page_size: int,
              date_from: Optional[datetime] = None,
              date_to: Optional[datetime] = None,
              tags: Optional[str] = None,
              keyword: Optional[str] = None,
              author_id: Optional[int] = None,
              session: Session = Depends(get_session)):
    posts = get_all_posts(
        session=session,
        page=page,
        page_size=page_size,
        date_from=date_from,
        date_to=date_to,
        tags=tags,
        keyword=keyword,
        author_id=author_id,
    )
    return posts


@router.get("/{post_id}/")
def get_post(post_id: int, session: Session = Depends(get_session)):
    return get_post_by_id(session, post_id)


@router.put("/{post_id}/")
def update_existing_post(post_id: int, title: str = None, content: str = None, tags: str = None,
                         session: Session = Depends(get_session), user=Depends(get_current_user)):
    get_post_by_id(session, post_id)
    check_role(user, ["Admin", "Author"])
    updated_post = update_post(session, post_id, user.role,user.id, title, content, tags)

    return {"message": "Post updated successfully", "post": updated_post} if updated_post else {"message": "not permission"}


@router.delete("/{post_id}/")
def delete_existing_post(post_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    get_post_by_id(session, post_id)
    check_role(user, ["Admin"])
    delete_post(session, post_id)
    return {"message": "Post deleted successfully"}

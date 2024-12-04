from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import aliased
from sqlmodel import Session, select, cast, DateTime

from models import Post, Comment, User


def create_post(session: Session, post_data: Post):
    session.add(post_data)
    session.commit()
    session.refresh(post_data)
    return post_data


def get_posts(session: Session, skip: int = 0, limit: int = 10, filters: dict = None):
    query = session.query(Post)
    if filters:
        if "tags" in filters:
            query = query.filter(Post.tags.contains(filters["tags"]))
        if "author_id" in filters:
            query = query.filter(Post.author_id == filters["author_id"])
        if "keyword" in filters:
            query = query.filter(Post.content.contains(filters["keyword"]))
    return query.offset(skip).limit(limit).all()


def get_post_by_id(session: Session, post_id: int):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def update_post(session: Session, post_id: int, role,author_id, title: str = None, content: str = None, tags=None):
    if role == "Admin":
        post = session.query(Post).filter(Post.id == post_id).first()
    else:
        post = session.query(Post).filter(Post.id == post_id, Post.author_id == author_id).first()
        if not post:
            return {"message": "Permission denied. This post does not belong to you."}
        else:
            post = post
    fields_to_update = {
        "title": title,
        "content": content,
        "tags": tags,
    }
    updated = False
    for field, new_value in fields_to_update.items():
        if new_value is not None and getattr(post, field) != new_value:
            setattr(post, field, new_value)
            updated = True
    if updated:
        post.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(post)
    return post


def delete_post(session: Session, post_id: int):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.query(Comment).filter(Comment.post_id == post_id).delete()
        session.delete(post)
        session.commit()
        return True
    return False


def get_all_users(session: Session):
    users = session.exec(select(User)).all()
    return users


def get_user_by_id(session: Session, user_id: int):
    user = session.get(User, user_id)
    return user


def get_all_posts(
        session: Session,
        page: int,
        page_size: int,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        tags: Optional[str] = None,
        keyword: Optional[str] = None,
        author_id: Optional[int] = None,
):
    query = select(Post, User.name, User.last_name).join(User, Post.author_id == User.id)

    if date_from:
        query = query.where(cast(Post.created_at, DateTime) >= date_from)
    if date_to:
        date_to = date_to + timedelta(days=1)
        query = query.where(cast(Post.created_at, DateTime) < date_to)
    if tags:
        query = query.where(Post.tags.contains(tags))
    if keyword:
        query = query.where(Post.title.contains(keyword) | Post.content.contains(keyword))
    if author_id:
        query = query.where(Post.author_id == author_id)
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = session.exec(query).all()

    posts_with_author = []
    for post, first_name, last_name in result:
        post_dict = post.dict()
        post_dict["author"] = {"name": first_name,
                               "last_name": last_name}
        posts_with_author.append(post_dict)
    if len(posts_with_author) == 0:
        return {"message": "not found!"}
    return posts_with_author


# comments
def create_comment(session: Session, post_id: int, content: str, author_id: int):
    new_comment = Comment(content=content, post_id=post_id, author_id=author_id, created_at=datetime.now())
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment


def get_comments_by_post(session: Session, post_id: int, role, author_id):
    if role == "Admin":
        return session.query(Comment).filter(Comment.post_id == post_id).all()
    if role == "Author":
        post = session.query(Post).filter(Post.id == post_id, Post.author_id == author_id).first()
        if not post:
            return {"message": "Permission denied. This post does not belong to you."}
        else:
            return session.query(Comment).filter(Comment.post_id == post_id).all()
    return {"message": "permission denied"}


def get_comments_by_post_and_author(session: Session, post_id: int, author_id: int):
    return session.query(Comment).filter(Comment.post_id == post_id, Comment.author_id == author_id).all()


def get_comment_by_id(session: Session, comment_id: int):
    comment = session.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


def update_comment(session: Session, comment, content: str):
    comment.content = content
    session.commit()
    session.refresh(comment)
    return comment


def delete_comment(session: Session, comment):
    session.delete(comment)
    session.commit()

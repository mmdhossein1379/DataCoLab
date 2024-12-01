from datetime import datetime
from typing import Optional

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
    return session.query(Post).filter(Post.id == post_id).first()


def update_post(session: Session, post_id: int, title: str = None, content: str = None, tags=None):
    post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    if title is not None:
        post.title = title
    if content is not None:
        post.content = content
    if tags is not None:
        post.tags = tags
    session.commit()
    session.refresh(post)
    return post


def delete_post(session: Session, post_id: int):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.delete(post)
        session.commit()
        return True
    return False


def create_comment(session: Session, comment_data: Comment):
    session.add(comment_data)
    session.commit()
    session.refresh(comment_data)
    return comment_data


def get_comments_for_post(session: Session, post_id: int):
    return session.query(Comment).filter(Comment.post_id == post_id).all()


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
        query = query.where(cast(Post.created_at, DateTime) <= date_to)
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
    return posts_with_author
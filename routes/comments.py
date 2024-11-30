from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_user, check_role
from models import Comment
from database import get_session
from crud import create_comment, get_comments_for_post, get_post_by_id

router = APIRouter()


@router.post("/")
def create_new_comment(post_id: int, content: str, session: Session = Depends(get_session),
                       user=Depends(get_current_user)):
    # بررسی نقش: همه نقش‌ها مجاز به افزودن کامنت هستند
    new_comment = Comment(content=content, post_id=post_id, author_id=user.id)
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return {"message": "Comment added successfully", "comment": new_comment}


@router.get("/{post_id}/")
def get_comments(post_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    post = get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Admin می‌تواند تمام کامنت‌ها را ببیند
    if user.role == "Admin":
        comments = session.query(Comment).filter(Comment.post_id == post_id).all()

    # Author فقط کامنت‌های مرتبط با پست‌های خودش را می‌بیند
    elif user.role == "Author":
        if post.author_id != user.id:
            raise HTTPException(status_code=403, detail="Permission denied")
        comments = session.query(Comment).filter(Comment.post_id == post_id).all()

    # Reader می‌تواند بدون محدودیت کامنت‌ها را مشاهده کند
    else:
        comments = session.query(Comment).filter(Comment.post_id == post_id).all()

    return comments

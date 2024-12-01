from database import get_session
from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user
from auth import check_role
from sqlalchemy.orm import Session
from crud import (
    create_comment,
    get_comments_by_post,
    get_comment_by_id,
    update_comment,
    delete_comment,
    get_post_by_id
)

router = APIRouter()


# create comment for special post
@router.post("/")
def create_new_comment(post_id: int, content: str, session: Session = Depends(get_session),
                       user=Depends(get_current_user)):
    check_role(user, ["Admin", "Reader"])
    get_post_by_id(session, post_id)
    new_comment = create_comment(session, post_id, content, user.id)
    return {"message": "Comment added successfully", "comment": new_comment}


# get comments for post
@router.get("/{post_id}/")
def get_comments(post_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    user_role = check_role(user, ["Admin", "Author"])
    get_post_by_id(session, post_id)
    if user_role is True:
        comments = get_comments_by_post(session, post_id,user.role,user.id)
    else:
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"comments": comments}


# edit_comment
@router.put("/{comment_id}/")
def edit_comment(comment_id: int, content: str, session: Session = Depends(get_session),
                 user=Depends(get_current_user)):
    user_role = check_role(user, ["Admin"])
    if user_role is True:
        comment = get_comment_by_id(session, comment_id)
        updated_comment = update_comment(session, comment, content)
        return {"message": "Comment updated successfully", "comment": updated_comment}
    return {"message": "Permission denied"}


# delete comment
@router.delete("/{comment_id}/")
def delete_comment_route(comment_id: int, session: Session = Depends(get_session),
                         user=Depends(get_current_user)):
    user_role = check_role(user, ["Admin"])
    if user_role is True:
        comment = get_comment_by_id(session, comment_id)
        delete_comment(session, comment)
    else:
        raise HTTPException(status_code=403, detail="Permission denied")

    return {"message": "Comment deleted successfully"}

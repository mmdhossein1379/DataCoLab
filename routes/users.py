from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_user, check_role
from models import User
from database import get_session
from crud import get_all_users, get_user_by_id

router = APIRouter()

@router.get("/")
def get_users(session: Session = Depends(get_session), user = Depends(get_current_user)):
    check_role(user, ["Admin"])
    users = get_all_users(session)
    return users

@router.get("/{user_id}/")
def get_user(user_id: int, session: Session = Depends(get_session), user = Depends(get_current_user)):
    check_role(user, ["Admin"])
    user_data = get_user_by_id(session, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data


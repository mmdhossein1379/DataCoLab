from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_user, check_role
from models import User
from database import get_session
from crud import get_all_users, get_user_by_id

router = APIRouter()

# دریافت لیست کاربران (فقط توسط ادمین)
@router.get("/")
def get_users(session: Session = Depends(get_session), user = Depends(get_current_user)):
    check_role(user, ["Admin"])
    users = get_all_users(session)
    return users

# دریافت جزئیات یک کاربر خاص (فقط توسط ادمین)
@router.get("/{user_id}/")
def get_user(user_id: int, session: Session = Depends(get_session), user = Depends(get_current_user)):
    check_role(user, ["Admin"])
    user_data = get_user_by_id(session, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

# دریافت پروفایل کاربر جاری
@router.get("/me/")
def get_my_profile(user = Depends(get_current_user)):
    return {"id": user.id, "username": user.username, "email": user.email, "role": user.role}

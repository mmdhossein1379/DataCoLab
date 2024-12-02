from sqlalchemy.orm import Session
from models import User
from auth import get_password_hash
from database import engine


def add_user(username: str, email: str, password: str, role: str,name,last_name):
    hashed_password = get_password_hash(password)
    user = User(username=username, email=email, password=hashed_password, role=role,name=name, last_name=last_name)

    with Session(engine) as session:
        session.add(user)
        session.commit()
        print(f"User '{username}' added with role '{role}'.")


# اضافه کردن کاربران
add_user("admin_user", "admin@gmail.com", "123", "Admin","mmd","ebi")
add_user("author_user", "author@gmail.com", "123", "Author","ali","ahmadi")
add_user("reader_user", "reader@gmail.com", "123", "Reader","hamid","hamidi")

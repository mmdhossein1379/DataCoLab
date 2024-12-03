from fastapi.testclient import TestClient
import sys
import os
import pytest
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from models import Comment, User, User
from crud import *
from main import app
from database import get_session

client = TestClient(app)


def get_auth_token():
    response = client.post(
        "/auth/token",
        data={"username": "admin_user", "password": "123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_create_new_comment():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/comments/?post_id=9&content=Simple%20test%20comment",
        json={"content": "This is a test comment"},
        headers=headers
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Comment added successfully"
    assert "comment" in response.json()

def test_edit_comment():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        "/comments/1/?content=Updatedcomment"
        , headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Comment updated successfully"
def test_get_comments():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/comments/9", headers=headers)
    assert response.status_code == 200
    assert "comments" in response.json()





# def test_delete_comment():
#     token = get_auth_token()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete("/comments/1/", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Comment deleted successfully"


def test_create_new_post():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/posts/",
        json={"title": "Updated Title", "content": "Updated Content", "tags": "updated,example","author_id":2}
        , headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Post created successfully"
    assert "post" in response.json()


def test_get_posts():
    response = client.get("/posts/?page=1&page_size=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_post():
    response = client.get("/posts/9/")
    assert response.status_code == 200
    assert "title" in response.json()
    assert "content" in response.json()


def test_update_existing_post():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        "/posts/9/",
        json={"title": "Updated Title", "content": "Updated Content", "tags": "updated,example","author_id":2}
        , headers=headers

    )
    assert response.status_code == 200
    assert response.json()["message"] == "Post updated successfully"
    assert "post" in response.json()

# def test_delete_existing_post():
#     token = get_auth_token()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.delete("/posts/1/", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Post deleted successfully"

import pytest
from datetime import datetime
from unittest.mock import MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from models import Comment, User
from crud import *


# ------------------------COMMENT_TEST__________________________________
def test_create_comment():
    session = MagicMock()
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()

    post_id = 1
    content = "Test comment"
    author_id = 123

    new_comment = create_comment(session, post_id, content, author_id)

    assert new_comment.content == content
    assert new_comment.post_id == post_id
    assert new_comment.author_id == author_id
    assert isinstance(new_comment.created_at, datetime)
    session.add.assert_called_once_with(new_comment)
    session.commit.assert_called_once()


def test_get_comment_by_id_found():
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = Comment(id=1, content="Test", post_id=1)

    comment = get_comment_by_id(session, 1)
    assert comment.id == 1
    assert comment.content == "Test"


def test_get_comment_by_id_not_found():
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_comment_by_id(session, 1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Comment not found"


def test_delete_comment():
    session = MagicMock()
    comment = Comment(id=1, content="Test", post_id=1)

    delete_comment(session, comment)

    session.delete.assert_called_once_with(comment)
    session.commit.assert_called_once()


# __________________________________POST_TEST__________________________________
def test_create_post():
    session = MagicMock()
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()

    new_post = Post(
        title="Test Title",
        content="Test Content",
        tags="test,example",
        author_id=1,
        created_at=datetime.utcnow(),
    )

    created_post = create_post(session, new_post)

    session.add.assert_called_once_with(new_post)
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(new_post)

    assert created_post.title == "Test Title"
    assert created_post.content == "Test Content"
    assert created_post.tags == "test,example"


def test_get_post_by_id_found():
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = Post(
        id=1, title="Test Title", content="Test Content"
    )

    post = get_post_by_id(session, 1)
    assert post.id == 1
    assert post.title == "Test Title"


def test_get_post_by_id_not_found():
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_post_by_id(session, 1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post not found"


def test_delete_post():
    session = MagicMock()
    post = Post(id=1, title="Test Title")

    delete_post(session, post.id)

    session.query.return_value.filter.return_value.delete.assert_called_once()
    session.commit.assert_called_once()

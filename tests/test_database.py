import pytest

from src.database import (  # , login_user, logout_user
    connect_to_db,
    create_user,
    get_user,
)

test_user_data = {
    "email": "test@email.com",
    "firstname": "test",
    "lastname": "email",
    "password": "somepassword",
}


@pytest.fixture
def db():
    return connect_to_db()


def test_get_user(db):
    """
    assuming user test@email.com is registered
    """
    create_user(test_user_data)
    user = get_user(test_user_data["email"])
    assert user["email"] == test_user_data["email"]
    assert user["password"] == "somepassword"
    import pdb

    pdb.set_trace()
    cleanup(db, test_user_data["email"])


def test_get_user_not_registered():
    """
    assuming user test@email.com isn't registered
    """
    test_email = "notregistered@email.com"
    user = get_user(test_email)
    assert user is None


def test_create_user(db):
    users = db["users"]
    cleanup(db, test_user_data["email"])

    query = {"email": test_user_data["email"]}

    assert users.find_one(query) is None

    response = create_user(test_user_data)

    assert users.find_one(query)

    response = create_user(test_user_data)

    assert response == "user already registered"

    users.delete_one(query)


def cleanup(db, email):
    users = db["users"]
    users.delete_one({"email": email})

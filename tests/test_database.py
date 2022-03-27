import pytest

from api_adapter.database import (
    connect_to_db,
    get_user,
    login_user,
    logout_user,
    register_user,
)
from api_adapter.helpers import encrypt_password

test_user_data = {
    "email": "test@email.com",
    "firstname": "test",
    "lastname": "email",
    "password": "somepassword",
}


def cleanup(db, email):
    users = db["users"]
    logged_in = db["logged_in"]

    users.delete_one({"email": email})
    logged_in.delete_one({"email": email})


@pytest.fixture
def db():
    return connect_to_db()


def test_get_user(db):
    register_user(test_user_data)
    user = get_user(test_user_data["email"])

    assert user["email"] == test_user_data["email"]
    assert user["password"] == encrypt_password(test_user_data["password"])

    cleanup(db, test_user_data["email"])


def test_get_user_not_registered(db):
    test_email = "notregistered@email.com"
    cleanup(db, test_email)
    user = get_user(test_email)

    assert user is None


def test_register_user(db):
    users = db["users"]
    cleanup(db, test_user_data["email"])
    query = {"email": test_user_data["email"]}

    assert users.find_one(query) is None

    response = register_user(test_user_data)

    assert users.find_one(query) is not None
    assert response == f"User {test_user_data['email']} registered"

    response = register_user(test_user_data)

    assert (
        response
        == f"An account with email: {test_user_data['email']} is already registered"
    )

    cleanup(db, test_user_data["email"])


def test_login_user(db):
    users = db["users"]
    logged_in = db["logged_in"]
    query = {"email": test_user_data["email"]}

    # Register but not logged in
    cleanup(db, test_user_data["email"])
    _ = register_user(test_user_data)

    assert users.find_one(query) is not None
    assert logged_in.find_one(query) is None

    token = login_user(test_user_data["email"], test_user_data["password"])
    logged_in_user = logged_in.find_one(query)

    assert token is not None
    assert logged_in_user["token"] == token
    assert logged_in_user["email"] == test_user_data["email"]


def test_login_user_wrong_password(db):
    users = db["users"]
    logged_in = db["logged_in"]
    query = {"email": test_user_data["email"]}
    cleanup(db, test_user_data["email"])
    _ = register_user(test_user_data)

    assert users.find_one(query) is not None
    assert logged_in.find_one(query) is None

    token = login_user(test_user_data["email"], "incorrect password")

    assert token is None
    assert logged_in.find_one(query) is None
    cleanup(db, test_user_data["email"])


def test_login_user_not_registered(db):
    users = db["users"]
    logged_in = db["logged_in"]
    query = {"email": test_user_data["email"]}
    cleanup(db, test_user_data["email"])
    assert users.find_one(query) is None
    token = login_user(test_user_data["email"], test_user_data["password"])

    assert token is None
    assert logged_in.find_one(query) is None
    cleanup(db, test_user_data["email"])


def test_login_user_already_logged_in(db):
    users = db["users"]
    logged_in = db["logged_in"]
    query = {"email": test_user_data["email"]}

    # Register but not logged in
    cleanup(db, test_user_data["email"])
    _ = register_user(test_user_data)

    assert users.find_one(query) is not None
    assert logged_in.find_one(query) is None

    token0 = login_user(test_user_data["email"], test_user_data["password"])
    logged_in_user = logged_in.find_one(query)

    assert token0 is not None
    assert logged_in_user["token"] == token0
    assert logged_in_user["email"] == test_user_data["email"]

    token1 = login_user(test_user_data["email"], test_user_data["password"])
    logged_in_user = logged_in.find_one(query)

    assert token1 is None
    assert logged_in_user["token"] != token1
    assert logged_in_user["token"] == token0
    assert logged_in_user["email"] == test_user_data["email"]
    cleanup(db, test_user_data["email"])


def test_logout_user(db):
    users = db["users"]
    logged_in = db["logged_in"]
    cleanup(db, test_user_data["email"])
    query = {"email": test_user_data["email"]}
    _ = register_user(test_user_data)

    assert users.find_one(query) is not None
    assert logged_in.find_one(query) is None

    token0 = login_user(test_user_data["email"], test_user_data["password"])
    logged_in_user = logged_in.find_one(query)

    assert token0 is not None
    assert logged_in_user["token"] == token0
    assert logged_in_user["email"] == test_user_data["email"]

    logout_user(test_user_data["email"], token0)

    logged_in_user = logged_in.find_one(query)

    assert logged_in_user is None
    cleanup(db, test_user_data["email"])


def test_logout_user_failed(db):
    users = db["users"]
    logged_in = db["logged_in"]
    cleanup(db, test_user_data["email"])
    query = {"email": test_user_data["email"]}
    _ = register_user(test_user_data)

    assert users.find_one(query) is not None
    assert logged_in.find_one(query) is None

    token0 = login_user(test_user_data["email"], test_user_data["password"])
    logged_in_user = logged_in.find_one(query)

    assert token0 is not None
    assert logged_in_user["token"] == token0
    assert logged_in_user["email"] == test_user_data["email"]

    logout_user(test_user_data["email"], "not a real token")

    logged_in_user = logged_in.find_one(query)

    assert logged_in_user["token"] == token0
    assert logged_in_user["email"] == test_user_data["email"]
    cleanup(db, test_user_data["email"])

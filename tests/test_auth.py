import pytest

from src.auth import signup, valid_email, valid_name, valid_password
from src.database import connect_to_db

test_user_data = {
    "email": "test@email.com",
    "firstname": "Test",
    "lastname": "Email",
    "password": "SomePassword123",
}


def cleanup(db, email):
    users = db["users"]
    logged_in = db["logged_in"]

    users.delete_one({"email": email})
    logged_in.delete_one({"email": email})


@pytest.fixture
def db():
    return connect_to_db()


def test_signup(db):
    users_collection = db["users"]
    logged_in_collection = db["logged_in"]
    cleanup(db, test_user_data["email"])
    query = {"email": test_user_data["email"]}

    assert users_collection.find_one(query) is None
    assert logged_in_collection.find_one(query) is None

    result = signup(test_user_data)

    assert users_collection.find_one(query) is not None
    assert logged_in_collection.find_one(query) is not None

    assert "token" in result
    assert result["msg"] == f"User {test_user_data['email']} registered"

    cleanup(db, test_user_data["email"])


def test_valid_email():
    assert valid_email("a1@b.co")
    assert valid_email("seng2021@gmail.com")

    assert not valid_email("@gmail.com")
    assert not valid_email("a@gmail")
    assert not valid_email("Someemailwithoutat")
    assert not valid_email("a @gmail.com")
    assert not valid_email("#$#@gmail.com")
    assert not valid_email("a@@@@@b.com")


def test_valid_password():
    assert valid_password("SomePassword123")
    assert valid_password("mYg0dabc")

    assert not valid_password("Ab12")
    assert not valid_password("somepassword123")
    assert not valid_password("SomePassword")
    assert not valid_password("mYg0d")


def test_valid_name():
    assert valid_name("Fredrick")
    assert valid_name("Fredrick-bob")
    assert valid_name("Gsp")

    assert not valid_name("")

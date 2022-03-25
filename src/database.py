from typing import Optional

from pymongo import MongoClient

from src.constants import DB_CLIENT_PREFIX, ENVOY

# from src.helpers import encrypt_password, generate_token


def connect_to_db():
    """
    Connect to db
    """
    client = MongoClient(f"{DB_CLIENT_PREFIX}{ENVOY}?retryWrites=true&w=majority")
    return client[ENVOY]


def get_user(email: str) -> Optional[dict]:
    """
    Searches users db to find user information using an email
    """
    db = connect_to_db()
    users = db["users"]
    return users.find_one({"email": email})


def register_user(user_data: dict) -> str:
    """
    Creates document in db containing users information including hashed password, returning a generated token
    """
    if get_user(user_data["email"]):
        return "user already registered"

    db = connect_to_db()

    email = user_data["email"]

    users = db["users"]
    users.insert_one(user_data)

    return f"User {email} registered"


def login_user(email: str, password: str) -> str:
    """
    Generates new token for user and saves to db and returns
    """
    # db = connect_to_db()
    token = ""
    return token


def logout_user(token: str) -> None:
    """
    Remove logged in entry from db
    """
    # db = connect_to_db()
    pass

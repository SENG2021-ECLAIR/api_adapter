import logging
from typing import Optional

from pymongo import MongoClient

from src.constants import DB_CLIENT_PREFIX, ENVOY
from src.helpers import generate_token


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
    db = connect_to_db()
    users = db["users"]
    query = {"email": email}

    user = users.find_one(query)

    if user is not None:
        if user["password"] != password:
            logging.error(f"Password incorrect for {email}")
            return

        logged_in = db["logged_in"]

        if (
            logged_in.find_one(query) is not None
            and logged_in.find_one(query)["email"] == email
        ):
            logging.error(f"{email} is already logged in.")
            return

        token = generate_token()
        logged_in.insert_one({"email": email, "token": token})

        return token
    logging.error(f"{email} is not a registered user.")


def logout_user(email: str, token: str) -> None:
    """
    Remove logged in entry from db
    """
    db = connect_to_db()
    logged_in = db["logged_in"]

    query = {"email": email}

    logged_in_user = logged_in.find_one(query)
    if logged_in_user is None:
        logging.error(f"{email} is not logged in")
        return
    if logged_in_user["token"] != token:
        logging.error(f"{token} doesn't belong to {email}")
        return

    logged_in.delete_one(query)


def db_cleanup():
    db = connect_to_db()
    users = db["users"]
    logged_in = db["logged_in"]

    users_data = users.delete_many({})
    logging.info(f"Removed {users_data.deleted_count} documents from users collection.")
    logged_in_data = logged_in.delete_many({})
    logging.info(
        f"Removed {logged_in_data.deleted_count} documents from logged_in collection."
    )

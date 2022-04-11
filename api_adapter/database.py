import logging
import random
import sys
from typing import Optional, Tuple

from pymongo import MongoClient

from api_adapter.constants import DB_CLIENT_PREFIX, ENVOY
from api_adapter.helpers import generate_token, get_customer_name, get_time


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
    db = connect_to_db()

    email = user_data["email"]
    user_data["invoices"] = []
    print(user_data)

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
            return None, f"Password incorrect for {email}"

        logged_in = db["logged_in"]
        logged_in_user = logged_in.find_one(query)

        if logged_in_user is not None and logged_in_user["email"] == email:
            existing_token = logged_in_user["token"]
            return existing_token, f"{email} is now logged in"

        token = generate_token()
        logged_in.insert_one({"email": email, "token": token})

        return token, f"{email} is now logged in"
    logging.error(f"{email} is not a registered user")
    return None, f"{email} is not a registered user"


def logout_user(email: str, token: str) -> str:
    """
    Remove logged in entry from db
    """
    db = connect_to_db()
    logged_in = db["logged_in"]

    query = {"email": email}

    logged_in_user = logged_in.find_one(query)
    if logged_in_user is None:
        logging.error(f"{email} is not logged in")
        return f"{email} is not logged in"
    if logged_in_user["token"] != token:
        logging.error(f"{token} doesn't belong to {email}")
        return f"{token} doesn't belong to {email}"

    logged_in.delete_one(query)
    return f"Successfully logged out {email}"


def store_invoice(token: str, invoice: str, method: str) -> str:
    db = connect_to_db()
    logged_in = db["logged_in"]
    logged_in_query = {"token": token}

    logged_in_user = logged_in.find_one(logged_in_query)
    if logged_in_user is None:
        logging.error("Need to login to store an invoice")
        return "Need to login to store an invoice"

    users = db["users"]
    users_query = {"email": logged_in_user["email"]}

    customer_name = get_customer_name(invoice)

    invoice_data = {
        "customer_name": customer_name,
        "timestamp": get_time(),
        "size": sys.getsizeof(invoice),
        "content": invoice,
        "method": method,
    }

    users.update_one(users_query, {"$push": {"invoices": invoice_data}})
    return f"Successfully created and stored invoice for {logged_in_user['email']}"


def get_invoices(token: str) -> Tuple[list, str]:
    db = connect_to_db()
    logged_in = db["logged_in"]
    logged_in_query = {"token": token}

    logged_in_user = logged_in.find_one(logged_in_query)
    if logged_in_user is None:
        logging.error("Need to login to get invoices")
        return ([], "Need to login to get invoices")
    users = db["users"]
    users_query = {"email": logged_in_user["email"]}

    user = users.find_one(users_query)
    created = []
    received = []
    for invoice in user["invoices"]:
        if invoice["method"] == "created":
            created.append(invoice)
        elif invoice["method"] == "received":
            received.append(invoice)
    return (
        {"created": created, "received": received},
        f"Successfully retreived invoices for {logged_in_user['email']}",
    )


hex_colors = [
    "#2292A4",
    "#D96C06",
    "#BDBF09",
    "#613DC1",
    "#9B5094",
    "#BB4430",
    "#645DD7",
    "#054A91",
    "#447604",
    "#9A275A",
    "#0CA4A5",
    "#EDB230",
    "#EE2E31",
    "#D8F793",
]


def get_user_profile_color(email: str) -> str:
    db = connect_to_db()
    users = db["users"]

    query = {"email": email}
    user = users.find_one(query)

    try:
        hex_color = user["hex_color"]
    except Exception:
        hex_color = random.choice(hex_colors)
        users.update_one(query, {"$set": {"hex_color": str(hex_color)}})

    return hex_color


def get_user_first_last_name(email: str) -> Tuple[str]:
    db = connect_to_db()
    users = db["users"]

    query = {"email": email}
    user = users.find_one(query)

    if user is None:
        return ("", "")

    return ("valid email", user["firstname"], user["lastname"])


def update_user_profile_color(email: str, new_color: str) -> str:
    db = connect_to_db()
    users = db["users"]
    query = {"email": email}

    user = users.find_one(query)

    if user is not None:
        users.update_one(query, {"$set": {"hex_color": new_color}})
        return "profile colour successfully updated"

    logging.error(f"{email} is not a registered user")
    return f"{email} is not a registered user"


def update_user_profile_firstname(email: str, new_firstname: str) -> str:
    db = connect_to_db()
    users = db["users"]
    query = {"email": email}

    user = users.find_one(query)

    if user is not None:
        users.update_one(query, {"$set": {"firstname": new_firstname}})
        return f"firstname successfully updated for ${email}"

    logging.error(f"{email} is not a registered user")
    return f"{email} is not a registered user"


def update_user_profile_lastname(email: str, new_lastname: str) -> str:
    db = connect_to_db()
    users = db["users"]
    query = {"email": email}

    user = users.find_one(query)

    if user is not None:
        users.update_one(query, {"$set": {"lastname": new_lastname}})
        return f"lastname successfully updated for ${email}"

    logging.error(f"{email} is not a registered user")
    return f"{email} is not a registered user"


def update_user_password(email: str, password: str, new_password: str) -> str:
    db = connect_to_db()
    users = db["users"]
    query = {"email": email}

    user = users.find_one(query)

    if user is not None:
        if user["password"] != password:
            logging.error(f"Password incorrect for {email}")
            return f"Password incorrect for {email}"

        if user["password"] == password:
            users.update_one(query, {"$set": {"password": new_password}})
            return "Password successfully updated"

    logging.error(f"{email} is not a registered user")
    return f"{email} is not a registered user"


def db_cleanup() -> int:
    db = connect_to_db()
    users = db["users"]
    logged_in = db["logged_in"]

    users_data = users.delete_many({})
    logging.info(f"Removed {users_data.deleted_count} documents from users collection")
    logged_in_data = logged_in.delete_many({})
    logging.info(
        f"Removed {logged_in_data.deleted_count} documents from logged_in collection"
    )
    return users_data.deleted_count, logged_in_data.deleted_count

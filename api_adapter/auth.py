import re

from api_adapter.database import login_user, register_user
from api_adapter.helpers import encrypt_password


def signup(user_data: dict) -> dict:
    """
    Signs up the user given some data about the user.

        Parameters:
            user_data: dict = {
                "email": "",
                "password": "",
                "firstname": "",
                "lastname": ""
            }

        Returns:
            data: dict = {
                message: string
                token: string
            }

    """
    if not valid_email(user_data["email"]):
        return {"msg": f"{user_data['email']} is not a valid email."}

    if not valid_password(user_data["password"]):
        return {
            "msg": "Password needs to be minimum 6 characters and contain at least 1 capital letter and 1 number"
        }

    if not valid_name(user_data["firstname"]) and user_data["lastname"]:
        return {"msg": "First and Last names must not be empty."}

    user_data["password"] = encrypt_password(user_data["password"])
    msg = register_user(user_data)
    token, _ = login_user(user_data["email"], user_data["password"])
    if token is not None:
        msg += " and logged in."
    return {"msg": msg, "token": token}


def login(credentials: dict) -> dict:
    """
    Logs the user into their account given a username and password and returns a token.

        Parameters:
            credentials: dict = {
                "email": string,
                "password": string
            }

        Returns:
            data: dict = {
                "message": string,
                "token": string
            }
    """

    if not valid_email(credentials["email"]):
        return {"msg": f"{credentials['email']} is not a valid email."}

    encrypted_password = encrypt_password(credentials["password"])

    token, msg = login_user(credentials["email"], encrypted_password)

    return {"msg": msg, "token": token}


def logout():
    pass


def valid_email(email: str) -> bool:
    """
    Validates Email given
    """
    email_regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    return True if re.search(email_regex, email) else False


def valid_password(password: str) -> bool:
    """
    Validates password given
    """
    if (
        any(x.isupper() for x in password)
        and any(x.islower() for x in password)
        and any(x.isdigit() for x in password)
        and len(password) >= 7
    ):
        return True
    return False


def valid_name(name: str) -> bool:
    """
    Validates name given
    """
    return len(name) >= 1

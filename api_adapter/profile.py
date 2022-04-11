from api_adapter.auth import valid_email, valid_password
from api_adapter.database import (
    get_user_first_last_name,
    get_user_profile_color,
    update_user_password,
    update_user_profile_color,
)
from api_adapter.helpers import encrypt_password


def profile_details(data: dict) -> dict:
    """
    Gets the user firstname, lastname, and randomly generated profile color
        Parameters:
            credentials: dict = {
                "email": string,
            }

        Returns:
            data: dict = {
                "color": string,
                "firstname": string
                "lastname": string
            }
    """
    color = get_user_profile_color(data["email"])
    msg, firstname, lastname = get_user_first_last_name(data["email"])

    return {"color": color, "firstname": firstname, "lastname": lastname}


def update_profile_colour(credentials: dict, new_color: str) -> str:
    """
    Updates password of user if valid, and current password matches
        Parameters:
            credentials: dict = {
                "email": string
            }
            "new_color": string

        Returns:
            data: dict = {
                "message": string,
            }
    """
    if not valid_email(credentials["email"]):
        return {"msg": f"{credentials['email']} is not a valid email"}

    msg = update_user_profile_color(credentials["email"], new_color)
    return {"msg": msg}


def reset_password(credentials: dict) -> str:
    """
    Updates password of user if valid, and current password matches
        Parameters:
            credentials: dict = {
                "email": string,
                "password": string,
                "new_password": string
            }

        Returns:
            data: dict = {
                "message": string,
            }
    """

    if not valid_email(credentials["email"]):
        return {"msg": f"{credentials['email']} is not a valid email"}

    encrypted_password = encrypt_password(credentials["password"])
    encrypted_new_password = encrypt_password(credentials["new_password"])

    if not valid_password(credentials["new_password"]):
        return {
            "msg": "Password needs to contain at least 6 characters, 1 capital letter, 1 lowercase letter and 1 number"
        }

    msg = update_user_password(
        credentials["email"], encrypted_password, encrypted_new_password
    )

    return {"msg": msg}


if __name__ == "__main__":
    print(profile_details({"email": "jb@gmail.com"}))
    print(update_profile_colour({"email": "jb@gmail.com"}, "#D8F793"))
    print(profile_details({"email": "jb@gmail.com"}))
"""
Endpoints that allows for the user to use the buttons:
    - create
    - render
    - send
    - login
    - log out
    - send
    - sign up
"""

import json
import logging

from flask import Flask, request
from flask_cors import CORS

from api_adapter.auth import login, logout, signup
from api_adapter.create import persist_invoice
from api_adapter.database import check_logged_in_token, db_cleanup
from api_adapter.listing import list_invoices
from api_adapter.profile import (
    profile_details,
    reset_password,
    update_profile_colour,
    update_profile_firstname,
    update_profile_lastname,
)
from api_adapter.render import get_render
from api_adapter.send import send_invoice
from api_adapter.render_json import form_json
from api_adapter.team import create_team, invite_member, list_team_members
from api_adapter.users import list_users

APP = Flask(__name__)
CORS(APP)

EMPTY_BODY_STRING = "YOU'VE GIVEN ME AN EMPTY BODY :("


@APP.route("/")
def default_route():
    return "Hello, World!"


@APP.route("/signup", methods=["POST"])
def signup_route():
    body = request.get_json()
    print(body)
    if (
        "email" not in body
        or "password" not in body
        or "firstname" not in body
        or "lastname" not in body
    ):
        return {"msg": "Needs email, password, firstname and lastname in body"}
    response = signup(body)
    return response


@APP.route("/login", methods=["POST"])
def login_route():
    body = request.get_json()
    if "email" not in body or "password" not in body:
        return {"msg": "Needs email and password in body"}
    response = login(body)
    return response


@APP.route("/logout", methods=["POST"])
def logout_route():
    body = request.get_json()
    if "token" not in body or "email" not in body:
        return {"msg": "Needs email and token in body"}
    response = logout(body)
    return response


@APP.route("/user/details", methods=["POST"])
def user_details_route():
    body = request.get_json()
    if "email" not in body:
        return {"msg": "Needs email in body"}
    response = profile_details(body)
    return response


@APP.route("/user/update/color", methods=["POST"])
def update_color_route():
    body = request.get_json()
    if "email" not in body:
        return {"msg": "Needs email in body"}
    response = update_profile_colour(body)
    return response


@APP.route("/user/update/firstname", methods=["POST"])
def update_firstname_route():
    body = request.get_json()
    if "email" not in body:
        return {"msg": "Needs email in body"}
    response = update_profile_firstname(body)
    return response


@APP.route("/user/update/lastname", methods=["POST"])
def update_lastname_route():
    body = request.get_json()
    if "email" not in body:
        return {"msg": "Needs email in body"}
    response = update_profile_lastname(body)
    return response


@APP.route("/user/update/password", methods=["POST"])
def update_password_route():
    body = request.get_json()
    if "password" not in body or "new_password" not in body:
        return {"msg": "Needs password in body"}
    response = reset_password(body)
    return response


@APP.route("/invoice/send", methods=["POST"])
def send_route():
    body = request.get_json()
    response = send_invoice(body)
    return response


@APP.route("/invoice/create", methods=["POST"])
def create_route():
    body = request.get_json()
    logging.error(body)
    if "token" not in body or "invoice_data" not in body:
        return {"msg": "Needs token and invoice_data"}
    response = persist_invoice(body["token"], body["invoice_data"])
    return json.dumps(response)


@APP.route("/invoice/list", methods=["GET"])
def list_invoices_route():
    token = request.headers.get("token")
    if token is None:
        return {"msg": "Needs token in headers"}
    response = list_invoices(token)
    return json.dumps(response)


@APP.route("/invoice/render", methods=["GET"])
def render_invoice_route():
    token = request.headers.get("token")
    address = request.headers.get("ubl_address")
    if token is None or address is None:
        return {"msg": "Needs token and invoice_id in headers"}
    response = form_json(address)
    return json.dumps(response)


@APP.route("/users/list", methods=["GET"])
def list_users_route():
    token = request.headers.get("token")
    if not check_logged_in_token(token):
        return {"msg": "Invalid token"}
    response = list_users()
    print(response)
    return json.dumps(response)


@APP.route("/team/create", methods=["POST"])
def team_create_route():
    token = request.headers.get("token")
    if not check_logged_in_token(token):
        return {"msg": "Invalid token"}
    body = request.get_json()
    if "team_name" not in body:
        return {"msg": "Needs team_name in the body."}
    response = create_team(token, body["team_name"])
    return response


@APP.route("/team/invite", methods=["POST"])
def team_invite_route():
    token = request.headers.get("token")
    if not check_logged_in_token(token):
        return {"msg": "Invalid token"}
    body = request.get_json()
    role = "Member"
    if "team_name" not in body:
        return {"msg": "Needs team_name in the body."}
    elif "invitee_email" not in body:
        return {"msg": "Needs invitee_email in the body."}
    elif "role" in body:
        role = body["role"]

    response = invite_member(body["team_name"], body["invitee_email"], role)

    logging.info(response)
    return response


@APP.route("/team/members", methods=["GET"])
def team_members_route():
    token = request.headers.get("token")
    if not check_logged_in_token(token):
        return {"msg": "Invalid token"}
    role = request.args.get("role")
    response = list_team_members(token, role)

    logging.info(response)
    return response


@APP.route("/test", methods=["POST"])
def test_route():
    body = request.get_json()
    return body


@APP.route("/cleanup", methods=["POST"])
def cleanup_route():
    # DEV ONLY ROUTE SHOULD
    # FIND A WAY TO REMOVE IN PROD
    users_val, logged_in_val = db_cleanup()
    res = {
        "msg": f"Removed #{users_val} entries from users and #{logged_in_val} entries from logged_in."
    }
    return res

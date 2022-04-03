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
from api_adapter.send import send_invoice
from flask_cors import CORS
from api_adapter.auth import login, logout, signup
from api_adapter.create import persist_invoice
from api_adapter.database import db_cleanup
from api_adapter.listing import list_invoices
from api_adapter.render import get_render

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


@APP.route("/send", methods=["POST"])
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
    invoice_id = request.headers.get("invoice_id")
    if token is None or invoice_id is None:
        return {"msg": "Needs token and invoice_id in headers"}
    response = get_render(token, int(invoice_id))
    return json.dumps(response)


@APP.route("/cleanup", methods=["POST"])
def cleanup_route():
    # DEV ONLY ROUTE SHOULD
    # FIND A WAY TO REMOVE IN PROD
    users_val, logged_in_val = db_cleanup()
    res = {
        "msg": f"Removed #{users_val} entries from users and #{logged_in_val} entries from logged_in."
    }
    return res

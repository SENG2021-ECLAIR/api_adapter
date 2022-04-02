"""
Endpoints that allows for the user to use the buttons:
    - create
    - render
    - send
    - login
    - log out
    - sign up
"""

import json
import logging

from flask import Flask, request
from flask_cors import CORS

from api_adapter.auth import login, logout, signup
from api_adapter.create import persist_invoice
from api_adapter.database import db_cleanup
from api_adapter.listing import list_invoices

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
    if body is None:
        return {"msg": EMPTY_BODY_STRING}
    response = signup(body)
    return response


@APP.route("/login", methods=["POST"])
def login_route():
    body = request.get_json()
    response = login(body)
    return response


@APP.route("/logout", methods=["POST"])
def logout_route():
    body = request.get_json()
    response = logout(body)
    return response


@APP.route("/invoice/create", methods=["POST"])
def create_route():
    body = request.get_json()
    logging.error(body)
    response = persist_invoice(body["token"], body["invoice_data"])
    return json.dumps(response)


@APP.route("/invoice/list", methods=["GET"])
def list_invoices_route():
    body = request.get_json()
    logging.error(body)
    response = list_invoices(body["token"])
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

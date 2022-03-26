from flask import Flask, request

from src.auth import signup
from src.database import db_cleanup

APP = Flask(__name__)


@APP.route("/")
def default_route():
    return "Hello, World!"


@APP.route("/signup", methods=["POST"])
def signup_route():
    data = request.get_json()
    res = signup(data)
    print(res)
    return ""


@APP.route("/cleanup", methods=["POST"])
def cleanup_route():
    # DEV ONLY ROUTE SHOULD
    # FIND A WAY TO REMOVE IN PROD
    db_cleanup()
    res = {"msg": "Removed all data stored in database."}
    return res

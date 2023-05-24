from flask import Blueprint, render_template
from flask_admin.contrib.peewee import ModelView

from .models import User, UserInfo

my_blueprint = Blueprint("my_blueprint", __name__)


@my_blueprint.route("/")
def index():
    return render_template("index.html")


@my_blueprint.route("/login")
def login():
    return render_template("login.html")

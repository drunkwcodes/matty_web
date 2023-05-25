from flask import Blueprint, render_template
from flask_admin.contrib.peewee import ModelView

from .models import User, UserInfo

mbp = Blueprint("mbp", __name__)


@mbp.route("/")
def index():
    return render_template("index.html")


@mbp.route("/login")
def login():
    return render_template("login.html")

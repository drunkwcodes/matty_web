from flask import Blueprint
from flask_admin.contrib.peewee import ModelView

from .models import User, UserInfo

my_blueprint = Blueprint("my_blueprint", __name__)


@my_blueprint.route("/")
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

import logging
from pathlib import Path

import flask_admin as fadmin
from flask import Blueprint, Flask, render_template
from flask_admin.contrib.peewee import ModelView

from matty_web.models import Post, User, UserInfo, init_db
from matty_web.utils import conf, init_data
from matty_web.views import mbp


class UserAdmin(ModelView):
    inline_models = (UserInfo,)


class PostAdmin(ModelView):
    # Visible columns in the list view
    column_exclude_list = ["text"]

    # List of columns that can be sorted. For 'user' column, use User.email as
    # a column.
    column_sortable_list = ("title", ("user", User.email), "date")

    # Full text search
    column_searchable_list = ("title", User.username)

    # Column filters
    column_filters = ("title", "date", User.username)

    form_ajax_refs = {"user": {"fields": (User.username, "email")}}


def main():
    init_data()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123456790"

    # setup logging
    log_file = Path(conf["data_folder"]) / "matty_web.log"
    logging.basicConfig(filename=log_file, filemode="a")
    logging.getLogger().setLevel(logging.DEBUG)

    # setup flask admin
    admin = fadmin.Admin(app, name="Matty WEB Admin")

    admin.add_view(UserAdmin(User))
    admin.add_view(PostAdmin(Post))

    # setup db
    init_db()

    # views
    adminbp = Blueprint("adminbp", __name__)

    @adminbp.route("/")
    def index():
        return render_template("index.html", admin_mode=True)

    app.register_blueprint(
        adminbp
    )  # the router will route to the first registered view.
    app.register_blueprint(mbp)

    app.run(debug=True)


if __name__ == "__main__":
    main()

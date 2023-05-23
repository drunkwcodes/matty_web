import logging
from pathlib import Path

import flask_admin as fadmin
from flask import Flask
from flask_admin.contrib.peewee import ModelView

from matty_web.models import Post, User, UserInfo
from matty_web.utils import conf, init_data
from matty_web.views import my_blueprint


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
    log_file = Path(conf["data_folder"]) / "matty_web.log"
    logging.basicConfig(filename=log_file, filemode="a")
    logging.getLogger().setLevel(logging.DEBUG)

    admin = fadmin.Admin(app, name="Example: Peewee")

    admin.add_view(UserAdmin(User))
    admin.add_view(PostAdmin(Post))

    try:
        User.create_table()
        UserInfo.create_table()
        Post.create_table()
    except Exception as e:
        logging.exception(e)
        print("Create table error. See log for more information.")
        # pass

    # views
    app.register_blueprint(my_blueprint)

    app.run(debug=True)


if __name__ == "__main__":
    main()

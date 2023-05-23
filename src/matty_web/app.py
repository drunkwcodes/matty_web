import logging
import os
import tomllib
from pathlib import Path

import flask_admin as fadmin
from flask import Flask

from matty_web.models import Post, User, UserInfo
from matty_web.utils import init_data
from matty_web.views import my_blueprint


def main():
    init_data()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123456790"

    logging.basicConfig(filename="matty_web.log", filemode="a")
    logging.getLogger().setLevel(logging.DEBUG)

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

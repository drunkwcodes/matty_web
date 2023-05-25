import logging
from pathlib import Path

from flask import Flask

from matty_web.models import init_db
from matty_web.utils import conf, init_data
from matty_web.views import mbp


def main():
    init_data()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123456790"

    # setup logging
    log_file = Path(conf["data_folder"]) / "matty_web.log"
    logging.basicConfig(filename=log_file, filemode="a")
    logging.getLogger().setLevel(logging.DEBUG)

    # setup db
    init_db()

    # views
    app.register_blueprint(mbp)

    app.run()


if __name__ == "__main__":
    main()

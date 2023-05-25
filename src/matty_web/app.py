import logging
from pathlib import Path

from flask import Flask

from matty_web.models import init_db
from matty_web.utils import conf, init_data, login_manager
from matty_web.views import mbp


def main():
    init_data()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123456790"  # 設置一個密鑰以進行會話加密

    # setup logging
    log_file = Path(conf["data_folder"]) / "matty_web.log"
    logging.basicConfig(filename=log_file, filemode="a")
    logging.getLogger().setLevel(logging.INFO)

    # setup flask login
    login_manager.init_app(app)

    # setup db
    init_db()

    # views
    app.register_blueprint(mbp)

    app.run()


if __name__ == "__main__":
    main()

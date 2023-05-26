import logging
from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from peewee import DoesNotExist

from .models import User, UserInfo
from .utils import conf, login_manager, verify_password

mbp = Blueprint("mbp", __name__)  # main bp

# files bp
fbp = Blueprint(
    "fbp",
    __name__,
    static_folder=Path(conf["data_folder"]) / "server_files",
    static_url_path="/files",
)


@mbp.route("/")
def index():
    logging.debug("test index")
    if current_user.is_authenticated:
        if current_user.picture:  # TODO: test pic
            return render_template(
                "index.html",
                pic=url_for(
                    "fbp.static", filename=f"profile_pic/{current_user.picture}"
                ),
            )
        else:
            return render_template(
                "index.html", pic=url_for("static", filename="Sample_User_Icon.png")
            )
    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get_by_id(user_id)
    except DoesNotExist:
        return None


@mbp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        email = request.form.get("email")  # form 用 name="email" 才抓得到
        password = request.form.get("password")
        next = request.args.get("next")
        user = User.get_or_none(User.email == email)

        if user:
            if not user.password:
                login_user(user)
                flash("Need to reset password.")
                return redirect(next or url_for("mbp.index"))
            elif verify_password(password=password, hashed_password=user.password):
                login_user(user)
                flash("Logged in successfully.")

                return redirect(next or url_for("mbp.index"))
            else:
                flash("Wrong password.")
                return redirect(url_for("mbp.login"))
        else:
            flash("Email incorrect.")
            return redirect(url_for("mbp.login"))  # TODO: 或是顯示錯誤訊息


@mbp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("mbp.index"))

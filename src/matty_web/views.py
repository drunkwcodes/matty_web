import logging
from pathlib import Path

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from peewee import DoesNotExist, IntegrityError

from .models import Profile, User, UserInfo
from .utils import conf, hash_password, login_manager, verify_password

mbp = Blueprint("mbp", __name__)  # main bp

# files bp
fbp = Blueprint(
    "fbp",
    __name__,
    static_folder=Path(conf["data_folder"]) / "server_files",
    static_url_path="/files",
)


def pic_url():
    if current_user.is_authenticated and current_user.picture:
        return url_for("fbp.static", filename=f"profile_pic/{current_user.picture}")
    else:
        return url_for("static", filename="Sample_User_Icon.png")


@mbp.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", pic=pic_url())
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
        next_url = request.args.get("next")
        return render_template("login.html", next_url=next_url)

    elif request.method == "POST":
        email = request.form.get("email")  # form 用 name="email" 才抓得到
        password = request.form.get("password")
        next_url = request.args.get("next")
        user = User.get_or_none(User.email == email)

        if user:
            if not user.password:
                login_user(user)
                flash("Need to reset password.")
                return redirect(next_url or url_for("mbp.reset_password"))

            elif verify_password(password=password, hashed_password=user.password):
                login_user(user)
                flash("Logged in successfully.")

                return redirect(next_url or url_for("mbp.index"))
            else:
                flash("Wrong password.")
                return redirect(url_for("mbp.login", next=next_url))
        else:
            flash("Email incorrect.")
            return redirect(url_for("mbp.login"))  # TODO: 或是顯示錯誤訊息


@mbp.route("/profile")
def profile_self():
    if not current_user.is_authenticated:
        return redirect(url_for("mbp.login", next="/profile"))
    return redirect(f"/profile/{current_user.id}")


@mbp.route("/profile/<int:user_id>")
def profile(user_id):
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist:
        abort(404)

    pf = Profile.get(Profile.user == user)
    if pf.is_public or current_user == user:
        return render_template("profile.html", pic=pic_url(), profile=pf)
    else:
        abort(404)  # TODO: custom 404


@mbp.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if not current_user.is_authenticated:
        abort(401)

    if request.method == "GET":
        pf = Profile.get(Profile.user == current_user)
        return render_template("edit_profile.html", pic=pic_url(), profile=pf)

    elif request.method == "POST":
        username = request.form.get("username")
        education = request.form.get("education")
        experience = request.form.get("experience")
        bio = request.form.get("bio")

        current_user.username = username
        try:
            current_user.save()
        except IntegrityError:
            flash("New username conflicts with existing account.")

        pf = Profile.get(Profile.user == current_user)
        pf.education = education
        pf.experience = experience
        pf.bio = bio
        pf.save()

        flash("Edit Successful!")
        return redirect(url_for("mbp.profile", user_id=current_user.id))


@mbp.route("/settings")
def settings():
    if not current_user.is_authenticated:
        abort(401)
    return render_template("settings.html", pic=pic_url())


@mbp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if not current_user.is_authenticated:
        abort(401)

    if request.method == "GET":
        return render_template("reset_password.html", pic=pic_url())

    elif request.method == "POST":
        new_password = request.form.get("new-password")
        confirm_password = request.form.get("confirm-password")

        assert new_password == confirm_password

        current_user.password = hash_password(new_password)
        current_user.save()

        flash("New password set!")

        return redirect(url_for("mbp.settings"))


@mbp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("mbp.index"))

import os
import random
import string
import tomllib
from pathlib import Path

import bcrypt
from flask_login import LoginManager

conf_file = Path(__file__).with_name("conf.toml")
with open(conf_file, "rb") as f:
    conf = tomllib.load(f)

login_manager = LoginManager()


def init_data():
    
    dpath = conf["data_folder"]
    if not os.path.exists(Path(dpath)):
        os.mkdir(dpath)

    # mkdir mbp static
    sfiles = Path(dpath)/ "server_files"
    if not os.path.exists(sfiles):
        os.mkdir(sfiles)

    # mkdir profile picture
    pp = Path(dpath)/ "server_files" / "profile_pic"
    if not os.path.exists(pp):
        os.mkdir(pp)

    # mkdir material files
    mf = Path(dpath)/ "server_files" / "materials"
    if not os.path.exists(mf):
        os.mkdir(mf)


def generate_password(length=5):
    clist = string.ascii_letters + string.digits
    pw = []
    for _ in range(length):
        pw.append(random.choice(clist))
    return "".join(pw)


def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password


def verify_password(password, hashed_password):
    # Check if the provided password matches the hashed password
    if type(password) is not bytes:
        password = password.encode("utf-8")

    if type(hashed_password) is not bytes:
        hashed_password = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password, hashed_password)

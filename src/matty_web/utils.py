import os
import random
import string
import tomllib
from pathlib import Path

import bcrypt

conf_file = Path(__file__).with_name("conf.toml")
with open(conf_file, "rb") as f:
    conf = tomllib.load(f)


def init_data():
    conf_file = Path(__file__).with_name("conf.toml")
    with open(conf_file, "rb") as f:
        conf = tomllib.load(f)
    dpath = conf["data_folder"]
    if not os.path.exists(Path(dpath)):
        os.mkdir(dpath)
    # TODO: mkdir profile picture


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
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

import os
import random
import string
import tomllib
from pathlib import Path

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

import os

from matty_web.models import User, add_user
from matty_web.utils import (
    conf,
    generate_password,
    hash_password,
    init_data,
    verify_password,
)


def test_init_data():
    init_data()
    assert os.path.exists(conf["data_folder"])


def test_generate_password():
    pw = generate_password()
    assert len(pw) == 5


def test_hash_password():
    pw = hash_password(generate_password())
    assert len(pw) == 60


def test_verify_password():
    pw = generate_password()
    hpw = hash_password(pw)
    assert verify_password(pw, hpw)

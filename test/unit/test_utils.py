import os

from matty_web.utils import conf, generate_password, init_data


def test_init_data():
    init_data()
    assert os.path.exists(conf["data_folder"])


def test_generate_password():
    pw = generate_password()
    assert len(pw) == 5

from matty_web.models import User, add_user, init_db


def test_add_user():
    init_db()
    add_user(username="drunkwcodes", email="eric@simutech.com.tw", password="123456")
    assert User.get(
        User.username == "drunkwcodes" and User.email == "eric@simutech.com.tw"
    )

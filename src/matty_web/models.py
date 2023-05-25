import logging
import tomllib
import uuid
from datetime import datetime
from pathlib import Path

import peewee
from flask_login import UserMixin

from .utils import conf, generate_password, hash_password

db_path = Path(conf["data_folder"]) / "test.sqlite"
db = peewee.SqliteDatabase(db_path, check_same_thread=False)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel, UserMixin):
    username = peewee.CharField(max_length=80)
    email = peewee.CharField(max_length=120)
    password = peewee.CharField(max_length=60, null=True)
    picture = peewee.CharField(max_length=120, null=True)
    add_at = peewee.TimeField()

    def __str__(self):
        return self.username


class UserInfo(BaseModel):
    key = peewee.CharField(max_length=64)
    value = peewee.CharField(max_length=64)

    user = peewee.ForeignKeyField(User)

    def __str__(self):
        return f"{self.key} - {self.value}"


class Post(BaseModel):
    id = peewee.UUIDField(primary_key=True, default=uuid.uuid4)
    title = peewee.CharField(max_length=120)
    text = peewee.TextField(null=False)
    date = peewee.DateTimeField()

    user = peewee.ForeignKeyField(User)

    def __str__(self):
        return self.title


def init_db():
    try:
        User.create_table()
        UserInfo.create_table()
        Post.create_table()
    except Exception as e:
        logging.exception(e)
        print("Create table error. See log for more information.")
        # pass


def add_user(username="", email="", password=""):
    if not username:
        raise Exception("username can not be empty.")
    if not email:
        raise Exception("email can not be empty.")

    # TODO: just return now when the email is registered before.
    if User.get_or_none(User.email == email):
        return

    if not password:
        password = generate_password()
        hpw = hash_password(password)
    else:
        hpw = hash_password(password)
    user = User(username=username, email=email, password=hpw, add_at=datetime.now())
    user.save()

    return user, password

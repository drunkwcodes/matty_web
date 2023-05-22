from flask import Flask
import flask_admin as fadmin
import peewee
import logging

from matty_web.models import User, UserInfo, Post
from matty_web.views import my_blueprint, UserAdmin, PostAdmin

def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123456790'



    logging.basicConfig(filename="matty_web.log", filemode="a")
    logging.getLogger().setLevel(logging.DEBUG)

    admin = fadmin.Admin(app, name='Example: Peewee')

    admin.add_view(UserAdmin(User))
    admin.add_view(PostAdmin(Post))

    try:
        User.create_table()
        UserInfo.create_table()
        Post.create_table()
    except Exception as e:
        logging.exception(e)
        print("Create table error. See log for more information.")
        # pass

    # views
    app.register_blueprint(my_blueprint)


    app.run(debug=True)

if __name__ == "__main__":
    main()

from flask import Blueprint
from flask_admin.contrib.peewee import ModelView

from .models import User, UserInfo

my_blueprint = Blueprint('my_blueprint', __name__)

class UserAdmin(ModelView):
    inline_models = (UserInfo,)


class PostAdmin(ModelView):
    # Visible columns in the list view
    column_exclude_list = ['text']

    # List of columns that can be sorted. For 'user' column, use User.email as
    # a column.
    column_sortable_list = ('title', ('user', User.email), 'date')

    # Full text search
    column_searchable_list = ('title', User.username)

    # Column filters
    column_filters = ('title',
                      'date',
                      User.username)

    form_ajax_refs = {
        'user': {
            'fields': (User.username, 'email')
        }
    }


@my_blueprint.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'
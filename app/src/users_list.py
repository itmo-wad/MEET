from flask import render_template
from flask.globals import session
from src.models import User

def users_list():
    current_user = User.get(session['user'])
    users = current_user.get_all()
    return render_template('/users/users.html', users=users)
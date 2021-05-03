from flask import render_template
from src.models import User

def users_list():
    users = User.get_all()
    return render_template('/users/users.html', users=users)
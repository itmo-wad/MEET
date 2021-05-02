from flask import session, render_template, redirect, url_for

from src.models import User

def cabinet():
    user = User.get_from_db(session['user'])
    return render_template('profile/profile.html', user=user)
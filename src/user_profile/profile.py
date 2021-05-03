from flask import request, render_template, redirect, session, url_for, abort
from src.authentication.utils import check_password, hash_password

from src.models import User

def cabinet(username):
    user_session = User.get_from_db(session['user'])
    find_user=User.get_from_db(username)
    username=user_session.username
    if not find_user:
        abort(404)
    user = find_user.username
    email = find_user.email
    fname = find_user.fname
    lname = find_user.lname
    if user==username:
        return render_template('profile/profile.html', username=username, email=email, lname=lname, fname=fname)
    else:
        return render_template('profile/profileGuest.html', username=username, email=email, lname=lname, fname=fname)


def changeProfile(username):
    user_session = User.get_from_db(session['user'])
    user = user_session.username
    if user !=username:
        return render_template(url_for('profile_page', username=username))
    if request.method == "POST" and user:
        email = request.form.get('email')
        password = request.form.get('password')
        password=hash_password(password)
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        user_session.update_db(email, fname, lname, password)
        return redirect(url_for('profile_page', username=username))
    return render_template('profile/changeProfile.html', username=username)
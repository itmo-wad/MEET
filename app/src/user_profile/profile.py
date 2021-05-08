from flask import request, render_template, redirect, session, url_for, abort

from src import friends
from src.authentication.utils import check_password, hash_password

from src.models import User


def cabinet(username):
    current_user = User.get(session['user'])
    requested_user = User.get(username)
    username = current_user.username
    if not requested_user:
        abort(404)
    user = requested_user.username
    if user == username:
        is_owner = True
        invites = friends.check_invites(user)
        return render_template('profile/profile.html', user=current_user, invites=invites, is_owner=is_owner)
    else:
        is_owner = False
        isInvited = friends.isInvited(requested_user.username, current_user.username)
        isInvitedByOther = friends.isInvited(current_user.username, requested_user.username)
        return render_template('profile/profile.html', user=requested_user, user_guest=current_user,
                               isInvited=isInvited, isInvitedByOther=isInvitedByOther, is_owner=is_owner)


def changeProfile(username):
    current_user = User.get(session['user'])
    user = current_user.username

    if user != username:
        return render_template(url_for('profile_page', username=username))

    if request.method == "POST" and user:

        email = request.form['email']
        if email and current_user.email != email:
            current_user.email = email

        old_password = request.form['old-password']
        password = request.form['password']
        if password and current_user.password != hash_password(password):
            if check_password(old_password, current_user.password):
                current_user.password = hash_password(password)

        fname = request.form['fname']
        if fname and current_user.fname != fname:
            current_user.fname = fname

        lname = request.form['lname']
        if lname and current_user.lname != lname:
            current_user.lname = lname

        current_user.update()

        return redirect(url_for('profile_page', username=current_user.username))
    return render_template('profile/changeProfile.html', user=current_user)
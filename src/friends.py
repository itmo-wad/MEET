from flask import url_for, render_template, session
from werkzeug.utils import redirect

from src.models import add_to_friendshipdb, find_from_friendship, delete_from_friendship, User, isInvited_in_db
import flask


def invite_friend(user_invited, user_inviting):
    add_to_friendshipdb(user_invited, user_inviting)
    return redirect(url_for('profile_page', username=user_invited))

def check_invites(username):
    invites=find_from_friendship(username)
    return invites

def isInvited(user_invited, user_inviting):
    answer=isInvited_in_db(user_invited, user_inviting)
    return answer



def add_to_friends(accept_user, user):
    user = User.get(user)
    accept_user = User.get(accept_user)
    if not user.friends:
        user.friends=[]
    if not accept_user.friends:
        accept_user.friends=[]
    user.friends.append(accept_user.username)
    user.update()
    accept_user.friends.append(user.username)
    accept_user.update()
    delete_from_friendship(accept_user.username, user.username)
    return redirect(url_for('profile_page', username=accept_user.username))
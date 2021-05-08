from flask import url_for, render_template, session
from werkzeug.utils import redirect

from src.models import Friends


def invite_friend(user_invited, user_inviting):
    friends = Friends(user_invited, user_inviting)
    friends.invite_friend()
    return redirect(url_for('profile_page', username=friends.user_invited))


def check_invites(username):
    invites = Friends.get_invitions(username)
    return invites


def isInvited(user_invited, user_inviting):
    answer = Friends.isInvited_in_db(user_invited, user_inviting)
    return answer

def cancel_ivition(cancelled_user, invited_user):
    Friends.cancel_invition(cancelled_user, invited_user)
    return redirect(url_for('profile_page', username=invited_user))


def add_to_friends(accept_user, user):
    Friends.add_to_friends(accept_user, user)
    return redirect(url_for('profile_page', username=accept_user))


def delete_friend(deleting_user, deleted_user):
    Friends.delete_friend(deleting_user, deleted_user)
    return redirect(url_for('profile_page', username=deleted_user))


def reject_the_invition(rejected_user, inviting_user):
    Friends.reject_the_invition(rejected_user, inviting_user)
    return redirect(url_for('profile_page', username=rejected_user))

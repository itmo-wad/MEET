from flask import Flask, render_template, redirect, url_for, session, request, make_response, flash

# Application modules
from src.authentication import auth
from src.authentication.auth import login_required
from src.user_profile import profile
from src.users_list import users_list
from src import friends
from src.avatar import getAvatar, updateAva, isPhoto
from src.models import User
import src.chat as chat

app = Flask(__name__)
app.secret_key = b'\xed\xe3\xdc\x18O\xcdS\xb6R\xb0\x8f\xd47\xa2\x87\xc7'


@app.route('/')
def index():
    return redirect('/register/')

# Authentication

@app.route('/register/', methods=['GET', 'POST'])
def register():
    return auth.register()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    return auth.login()


@app.route('/logout/', methods=['GET'])
def logout():
    return auth.logout()

# Profile

@app.route('/profile/<username>/', methods = ['GET'])
@login_required
def profile_page(username):
    return profile.cabinet(username)


@app.route('/profile/<username>/changeProfile/', methods=['GET', 'POST'])
@login_required
def change_profile(username):
    return profile.changeProfile(username)

# Friendship

@app.route('/invite_to_friends/', methods = ['GET'])
@login_required
def invite_to_friends():
    user_invited = request.args.get('user_invited')
    user_inviting = request.args.get('user_inviting')
    return friends.invite_friend(user_invited, user_inviting)


@app.route('/add_to_friends/', methods=['GET'])
def add_to_friends():
    accept_user = request.args.get('accept_user')
    inviting_user = request.args.get('inviting_user')
    return friends.add_to_friends(accept_user, inviting_user)


# List of users

@app.route('/users/', methods=['GET'])
@login_required
def users():
    return users_list()

# Chat

@app.route('/chat/', methods=['GET'])
@login_required
def chat_page():
    return chat.chat()

@app.route('/get_messages/<username>/', methods=['GET'])
@login_required
def messages(username):
    return chat.get_messages_from(username)

@app.route('/send_message/<username>/', methods=['POST'])
@login_required
def send_message(username):
    return chat.send_message(username)

@app.route('/upload/', methods=['POST', 'GET'])
@login_required
def upload():
    username = request.args.get('username')
    if request.method == 'POST':
        file = request.files['file']
        if file and isPhoto(file.filename):
            try:
                img = file.read()
                res = updateAva(username, img)
                if not res:
                    flash("Error of updating avatar", category="error")
                flash("Avatar updated successfully", category="success")
            except FileNotFoundError:
                flash("Error of reading file", "error")
        else:
            flash("Error of updating avatar", "error")
        return redirect(url_for('profile_page', username=username))


@app.route('/userava/', methods=['GET'])
def userava():
    username = request.args.get('username')
    img = getAvatar(username, app)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/cancel_invition/', methods=['GET'])
def cancel_invition():
    cancelled_user = request.args.get('cancelled_user')
    invited_user = request.args.get('invited_user')
    return friends.cancel_ivition(cancelled_user, invited_user)


@app.route('/delete_friend/', methods=['GET'])
def delete_friend():
    deleting_user = request.args.get('deleting_user')
    deleted_user = request.args.get('deleted_user')
    return friends.delete_friend(deleting_user, deleted_user)


@app.route('/reject/', methods=['GET'])
def reject():
    rejected_user = request.args.get('rejected_user')
    inviting_user = request.args.get('inviting_user')
    return friends.reject_the_invition(rejected_user, inviting_user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
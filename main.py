from flask import Flask, render_template, redirect, request

# Application modules
from src.authentication import auth
from src.authentication.auth import login_required
from src.user_profile import profile
from src.users_list import users_list
import src.friends as friends
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

@app.route('/logout/', methods = ['GET'])
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
    user_invited=request.args.get('user_invited')
    user_inviting=request.args.get('user_inviting')
    return friends.invite_friend(user_invited, user_inviting)

@app.route('/add_to_friends/',  methods = ['GET'])
def add_to_friends():
    accept_user = request.args.get('accept_user')
    inviting_user = request.args.get('inviting_user')
    return  friends.add_to_friends(accept_user, inviting_user)

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
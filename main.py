from src.models import User
from flask import Flask, render_template, redirect, url_for, session

# Application modules
from src.authentication import auth
from src.authentication.auth import login_required
from src.user_profile import profile
from src.users_list import users_list

app = Flask(__name__)
app.secret_key = b'\xed\xe3\xdc\x18O\xcdS\xb6R\xb0\x8f\xd47\xa2\x87\xc7'

@app.route('/')
def index():
    return redirect('/register/')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    return auth.register()

@app.route('/login/', methods=['GET', 'POST'])
def login():
    return auth.login()

@app.route('/logout/', methods = ['GET'])
def logout():
    return auth.logout()

@app.route('/profile/<username>/', methods = ['GET'])
@login_required
def profile_page(username):
    return profile.cabinet(username)

@app.route('/profile/<username>/changeProfile/', methods=['GET', 'POST'])
@login_required
def change_profile(username):
    return profile.changeProfile(username)

@app.route('/users/')
@login_required
def users():
    return users_list()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)

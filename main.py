from src.models import User
from flask import Flask, render_template, request, redirect, url_for, session

# Application modules
from src.authentication import auth

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


@app.route('/profile/', methods = ['GET'])
def profile():
    if 'user' in session:
        user = User.get_from_db(session['user'])
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('register'))

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.meet_db
    app.run(host='localhost', port=5000, debug=True)

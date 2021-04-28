from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        password = request.form.get('password')
        password_retry = request.form.get('password-retry')
        
        if password == password_retry:
            db.users.insert_one(
                {"username": username, "email": email, "fname": fname, "lname": lname, "password": password})
            return redirect(url_for('profile', username=username))
        else:
            return redirect(url_for('register'))

@app.route('/profile/', methods = ['GET'])
def profile():
    username = request.args.get('username')
    return render_template('profile.html', username=username)

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.meet_db
    app.run(host='localhost', port=5000, debug=True)

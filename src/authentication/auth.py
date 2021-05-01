from flask import request, render_template, redirect, session, url_for

from src.models import User
from src.authentication.utils import check_password, hash_password

def register():    
    if request.method == 'POST':
        password = request.form['password']
        password_retry = request.form['password-retry']
        username = request.form['username']
        email = request.form['email']
        
        if User.get_from_db(username) == None: 
            if password == password_retry:
                user = User(
                    username = username,
                    email = email,
                    password = hash_password(password)
                )
                user.insert_to_db()
                session['user'] = user.username        
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('register'))
    return render_template('register.html')

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.get_from_db(username)
        if user != None:
            if check_password(password, user.password):
                session['user'] = user.username
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))
    return render_template('login.html')

def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
from flask import render_template, request
from flask.globals import session
from datetime import datetime

from src.models import Message, User

def chat():
    current_user = User.get(session['user'])
    friends = current_user.friends
    return render_template('/chat/chat.html', friends=friends)

def get_messages_from(username):
    current_user = User.get(session['user'])
    messages = current_user.get_messages()
    if messages is not None:
        messages_from_user = [m for m in messages if m.recipient == username or m.sender == username]
        if messages_from_user != []:
            return render_template('/chat/messages.html', messages=messages_from_user, user=current_user)
    return render_template('/chat/no_messages.html')
    
    
def send_message(username):
    current_user = User.get(session['user'])
    
    message_text = request.form['message']
    current_date = datetime.now()

    new_message = Message(
        sender=current_user.username,
        recipient=username,
        text=message_text,
        creation_time=current_date
    )

    new_message.insert()
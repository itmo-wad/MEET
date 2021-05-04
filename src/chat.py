from flask import render_template

from src.models import User

def chat():
    users = User.get_all()
    return render_template('/chat/chat.html', users=users)


def send_message():
    print()
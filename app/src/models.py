from pymongo import MongoClient
import pymongo

# Database connection
client = MongoClient('mongodb', 27017)
db = client.meet_db

class User:
    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.fname = kwargs.get('fname')
        self.lname = kwargs.get('lname')
        self.friends = kwargs.get('friends')
    
    @staticmethod
    def __dict_to_user(data):
        user = User(
                username = data['username'],
                email = data['email'],
                password = data['password'],
                fname = data['fname'],
                lname = data['lname'],
                friends = data['friends']
            )
        if not user.friends:
            user.friends = []
        return user

    @staticmethod
    def get(username):
        user_data = db.users.find_one({'username': username})
        if user_data == None:
            return None
        else:
            return User.__dict_to_user(user_data)
    
    def insert(self):
        db.users.insert(vars(self))
    
    def update(self):
        db.users.update_one({'username': self.username}, {'$set': vars(self)})

    def get_all(self):
        users_data = db.users.find({'username': {'$ne': self.username}})
        users = []

        for item in users_data:
            users.append(User.__dict_to_user(item))

        return users
    
    def get_messages(self):
        return Message.get_for_user(self)

class Message:
    def __init__(self, **kwargs):
        self.sender = kwargs.get('sender')
        self.recipient = kwargs.get('recipient')
        self.text = kwargs.get('text')
        self.creation_time = kwargs.get('creation_time')

    def insert(self):
        db.messages.insert(vars(self))
    
    @staticmethod
    def __dict_to_message(data):
        message = Message(
            sender = data['sender'],
            recipient = data['recipient'],
            text = data['text'],
            creation_time = data['creation_time']
        )
        return message
    
    @staticmethod
    def get_for_user(user):
        messages_data = db.messages.find({'$or':[{'sender': user.username}, {'recipient': user.username}]}).sort('creation_time', pymongo.ASCENDING)
        messages = []

        for item in messages_data:
            messages.append(Message.__dict_to_message(item))  
        return messages
        
        
class Friends:
    def __init__(self, user_invited, user_inviting):
        self.user_invited = user_invited
        self.user_inviting = user_inviting
        self.status = False

    def add_to_friendshipdb(self):
        user = db.friendship.find_one({"user_inviting": self.user_inviting, "user_invited": self.user_invited})
        if user == None:
            db.friendship.insert(
                {"user_inviting": self.user_inviting, "user_invited": self.user_invited, "isAccepted": self.status})

    def invite_friend(self):
        self.add_to_friendshipdb()

    @staticmethod
    def __dict_to_friends(friend_data):
        friends = Friends(user_invited=friend_data['user_invited'], user_inviting=friend_data['user_inviting'])
        return friends

    @staticmethod
    def get_invitions(username):
        invitionList = []
        data = db.friendship.find({"user_invited": username})
        for invite in data:
            invitionList.append(invite)
        return invitionList

    @staticmethod
    def get_from_frienship(user_invited, user_inviting):
        friend_data = db.friendship.find_one({'user_invited': user_invited, 'user_inviting': user_inviting})
        if friend_data == None:
            return None
        else:
            return Friends.__dict_to_friends(friend_data)

    @staticmethod
    def isInvited_in_db(user_invited, user_inviting):
        friends = Friends.get_from_frienship(user_invited, user_inviting)
        if friends == None:
            return False
        else:
            return True

    @staticmethod
    def delete_from_friendship(username_invited, username_inviting):
        db.friendship.remove({"user_inviting": username_inviting, "user_invited": username_invited})

    @staticmethod
    def add_to_friends(accept_user, user):
        user = User.get(user)
        accept_user = User.get(accept_user)
        user.friends.append(accept_user.username)
        user.update()
        accept_user.friends.append(user.username)
        accept_user.update()
        Friends.delete_from_friendship(accept_user.username, user.username)

    @staticmethod
    def delete_friend(user_1, user_2):
        deleting_user = User.get(user_1)
        deleted_user = User.get(user_2)
        deleting_user.friends.remove(user_2)
        deleted_user.friends.remove(user_1)
        deleted_user.update()
        deleting_user.update()

    @staticmethod
    def reject_the_invition(rejecting_user, inviting_user):
        Friends.delete_from_friendship(rejecting_user, inviting_user)

    @staticmethod
    def cancel_invition(cancelled_user, invited_user):
        Friends.delete_from_friendship(invited_user, cancelled_user)

from pymongo import MongoClient

# Database connection
client = MongoClient('localhost', 27017)
db = client.meet_db

class User:
    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.fname = kwargs.get('fname')
        self.lname = kwargs.get('lname')
    
    @staticmethod
    def __dict_to_user(data):
        user = User(
                username = data['username'],
                email = data['email'],
                password = data['password'],
                fname = data['fname'],
                lname = data['lname']
            )
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

class Message:
    def __init__(self, **kwargs):
        self.sender = kwargs.get('sender')
        self.recipient = kwargs.get('recipient')
        self.text = kwargs.get('text')
        self.creation_time = kwargs.get('creation_time')

    def send(self):
        db.messages.insert(vars(self))
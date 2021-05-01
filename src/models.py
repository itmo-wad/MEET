import os
from pymongo import MongoClient

# Database connection
client = MongoClient('localhost', 27017)
db = client.meet_db

class User:
    def __init__(self, **kwargs):
        self._id = os.urandom(12).hex()
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.fname = kwargs.get('fname')
        self.lname = kwargs.get('lname')

    @staticmethod
    def get_from_db(username):
        query_result = db.users.find_one({'username': username})
        if query_result == None:
            return None
        else:
            user = User(
                _id = query_result['_id'],
                username = query_result['username'],
                email = query_result['email'],
                password = query_result['password'],
                fname = query_result['fname'],
                lname = query_result['lname']
            )
            return user
    
    def insert_to_db(self):
        db.users.insert(vars(self))
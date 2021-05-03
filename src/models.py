import os
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
    def get_from_db(username):
        query_result = db.users.find_one({'username': username})
        if query_result == None:
            return None
        else:
            user = User(
                username = query_result['username'],
                email = query_result['email'],
                password = query_result['password'],
                fname = query_result['fname'],
                lname = query_result['lname']
            )
            return user
    
    def insert_to_db(self):
        db.users.insert(vars(self))
    def update_db(self, email, fname, lname, password):
        if not password:
            password=self.password
        if not email:
            email=self.email
        if not fname:
            fname=self.fname
        if not lname:
            lname=self.lname
        db.users.update_one({'username': self.username}, {'$set': {'email':email, 'password':password, 'fname':fname, 'lname':lname}})
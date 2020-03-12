from flask_login import UserMixin
from flask_mongoengine import MongoEngine


db = MongoEngine()


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    social_id = db.IntField(max_length=64)

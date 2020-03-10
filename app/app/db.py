from flask_login import UserMixin
from flask_mongoengine import MongoEngine


db = MongoEngine()


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    email = db.StringField(max_length=30)
    social_id = db.IntField(max_length=64)
    image_url = db.StringField()
    friends_count = db.IntField()

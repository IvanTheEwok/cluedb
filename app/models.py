from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<User {}>".format(self.username)

class Clue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tier = db.Column(db.String(6))
    value = db.Column(db.Integer)
    stages = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Clue {id}, {tier}>".format(id=self.id, tier=self.tier)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    value_each = db.Column(db.Integer)
    clue_id = db.Column(db.Integer, db.ForeignKey("clue.id"))

    def __repr__(self):
        return "<Item {item}, amount {amount}>".format(item=self.item, amount=self.amount)
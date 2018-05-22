from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    clues = db.relationship("Clue", backref="player", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Clue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tier = db.Column(db.String(6))
    value = db.Column(db.Integer)
    stages = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    items = db.relationship("Item", backref="clue", lazy="dynamic")

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
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
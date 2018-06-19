from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin

followers = db.Table(
    "followers",
    db.Column(
        "follower_id",
        db.Integer,
        db.ForeignKey("user.id")),
    db.Column(
        "followed_id",
        db.Integer,
        db.ForeignKey("user.id"))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    clues = db.relationship("Clue", backref="player", lazy="dynamic", cascade="delete")
    followed = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic"
    )

    def __repr__(self):
        return "<User {}>".format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest,
            size
        )
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        followed = Clue.query.join(
            followers,
            (followers.c.follower_id == Clue.user_id)
        ).filter(
            followers.c.follower_id == self.id
        )
        own = Clue.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Clue.timestamp.desc())

class Clue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rsn = db.Column(db.String(20))
    tier = db.Column(db.String(6))
    value = db.Column(db.Integer)
    stages = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    items = db.relationship("Item", backref="clue", lazy="dynamic", cascade="delete")

    def __repr__(self):
        return "<Clue {id}, {tier}>".format(id=self.id, tier=self.tier)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    rs_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    value_each = db.Column(db.Integer)
    clue_id = db.Column(db.Integer, db.ForeignKey("clue.id"))

    def __repr__(self):
        return "<Item {item}, amount {amount}>".format(item=self.item, amount=self.amount)

class Rs_items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

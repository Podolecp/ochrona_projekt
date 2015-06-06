__author__ = 'Antah'
import bcrypt
from ochrona import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.pw_hash = bcrypt.hashpw(password, salt)

    def check_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), self.pw_hash.encode('utf-8')) == self.pw_hash.encode('utf-8')

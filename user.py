__author__ = 'Antah'
import bcrypt

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.pw_hash = bcrypt.hashpw(password, salt)

    def check_password(self, password):
        return bcrypt.hashpw(password, self.pw_hash) == self.pw_hash
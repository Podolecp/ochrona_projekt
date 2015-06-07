__author__ = 'Antah'
import bcrypt
from Crypto.Hash import SHA256

class User():

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.salt

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.salt = Crypto.Random.get_random_bytes(16)
        pwtmp = bcrypt.hashpw(password, salt)
        print pwtmp
        salt = bcrypt.gensalt()
        pwtmp = pwtmp + password
        self.pw_hash = bcrypt.hashpw(pwtmp, salt)
        print self.pw_hash



    def check_password(self, password):
        pwtmp = bcrypt.hashpw(password.encode('utf-8'), self.pw_hash.encode('utf-8'))
        print pwtmp
        pwtmp = pwtmp + password.encode('utf-8')
        pwtmp2 = bcrypt.hashpw(pwtmp, self.pw_hash.encode('utf-8'))
        print pwtmp2
        return pwtmp2 == self.pw_hash.encode('utf-8')

admin = User('admin','qwe')
print admin.check_password('qwe')
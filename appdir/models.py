from appdir import db, login, key
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(12), index= True, unique= True)
    email = db.Column(db.String(120), index= True, unique= True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    
    sent_messages = db.relationship('Message', back_populates='sender',lazy='dynamic', foreign_keys='Message.sender_id')
    received_messages = db.relationship('Message', back_populates='recipient',lazy='dynamic', foreign_keys='Message.recipient_id')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key = True)
    content_crypt = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    sender = db.relationship('User', back_populates='sent_messages', primaryjoin='Message.sender_id == User.id')
    recipient = db.relationship('User', back_populates='received_messages', primaryjoin='Message.recipient_id == User.id')
   
    def decrypted_message(self):
        f = Fernet(key)
        return f.decrypt(self.content_crypt.encode()).decode('utf-8')



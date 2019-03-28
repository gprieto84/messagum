import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'something really odd in the house'
    ENCRYPT_KEY = os.environ.get('ENCRYPT_KEY')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or "postgresql://localhost:5432/messagum"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
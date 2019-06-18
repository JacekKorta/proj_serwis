import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-long-password'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'your_server_adres'
    MAIL_PORT = 587
    #MAIL_USE_TLS = True
    #MAIL_USE_SSL = 1
    MAIL_USERNAME = 'username@mail.com'
    MAIL_PASSWORD = 'your_funny_password'
    OFFICE = ['office@mail.com']
    WAREHOUSE = ['warehouse@mail.com']
    SENDER = ['sender@mail.com']

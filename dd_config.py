import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-long-password'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'mail.draftstudio.pl'
    MAIL_PORT = 587
    #MAIL_USE_TLS = True
    #MAIL_USE_SSL = 1
    MAIL_USERNAME = 'info@janome.pl'
    MAIL_PASSWORD = 'Janome-Polska=info2194'
    OFFICE = ['info@janome.pl']
    WAREHOUSE = ['j.korta@janome.pl']
    SENDER = ['info@janome.pl']

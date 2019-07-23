import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'other_password'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    VERSION = '0.4'

    MAIL_SERVER = 'your_mail_server'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #MAIL_USE_SSL = True
    MAIL_USERNAME = 'your_login'
    MAIL_PASSWORD = 'your_mail_password'
    OFFICE = ['address_for_office_type_users']
    WAREHOUSE = ['address_for_warehouse_type_users']
    SENDER = ['your_mail_adres']

    ISSUES_PER_PAGE = 25
    CUSTOMERS_PER_PAGE = 200
    MACHINES_PER_PAGE = 200
    EVENTS_PER_PAGE = 25


from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(64))
    owner_name = db.relationship('Issues', backref='owner_name', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Issues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    owner = db.Column(db.String(32), db.ForeignKey('user.username'), nullable=False)
    machine_model = db.Column(db.String(64), index=True)
    serial_number = db.Column(db.String(16))
    part_number = db.Column(db.String(32), index=True)
    quantity = db.Column(db.Integer)
    part_name = db.Column(db.String(128), index=True)
    issue_desc = db.Column(db.String(256))
    where_is_part = db.Column(db.String(32), index=True)
    exchange_status = db.Column(db.String(32), index=True)
    janome_status = db.Column(db.String(32), index=True)
    comment = db.Column(db.String(128))
    customer_delivery_time = db.Column(db.String(32), index=True)
    delivery_time = db.Column(db.String(32), index=True)

    def __repr__(self):
        return'<Zgłoszenie {}, Produkt: {}, do maszyny: {}, o numerze seryjnym: {}>'.format(
            self.id, self.part_number, self.machines_model, self.serial_number)

class Machines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(56), index=True)

    def __repr__(self):
        return ' <id {}, Nazwa: {}>'.format(self.id, self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

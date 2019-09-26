from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(64))
    owner_name = db.relationship('Issues', backref='owner_name', lazy=True)
    event_owner = db.relationship('Events', backref='event_owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User_id: {}; username: {}; email: {}; user_type: {}>'.format(
            self.id,
            self.username,
            self.email,
            self.user_type)


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
        return'<Id: {}; machine_model: {}; serial_number: {}; product_num: {}, part_name: {};\
        issue_desc: {}; where_is_part: {}; exchange_status: {}; janome_status: {}; comment: {}; delivery_time: {}>'\
            .format(
            self.id,
            self.machine_model,
            self.serial_number,
            self.part_number,
            self.part_name,
            self.issue_desc,
            self.where_is_part,
            self.exchange_status,
            self.janome_status,
            self.comment,
            self.delivery_time)


class Machines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(56), index=True)

    def __repr__(self):
        return '<id: {}; Name: {}>'.format(self.id, self.name)


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(36), index=True, unique=True)
    name = db.Column(db.String(126))
    phone_num = db.Column(db.String(20))
    phone2_num = db.Column(db.String(20))
    email = db.Column(db.String(48), unique=True)

    def __repr__(self):
        return '<id: {}; code: {}; name: {}; phone_num: {}; phone2_num: {}; email: {}>'.format(
            self.id, self.code, self.name, self.phone_num, self.phone2_num, self.email)


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user = db.Column(db.String(32), db.ForeignKey('user.username'))
    description = db.Column(db.String(256))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

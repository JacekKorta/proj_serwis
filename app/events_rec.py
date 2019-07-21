from app.models import Events
from app import db

def events_rec (current_user, description):
    event = Events(user=current_user, description=description)
    db.session.add(event)
    db.session.commit()


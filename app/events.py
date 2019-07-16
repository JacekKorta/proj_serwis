from app.models import Events
from app import db

def events_rec (current_user, description):
    event = Events(user=current_user, description=description)
    db.session.add(event)
    db.session.commit()

'''
def events_rec_wraper(func):
    def inner_func(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return inner_func
'''

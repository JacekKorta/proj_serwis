from app import app, db
from app.models import User, Issues


@app.shell_context_processor
def make_shell_context():
    return{'db': db, 'User': User, 'Issues': Issues}


app.run(debug=True)
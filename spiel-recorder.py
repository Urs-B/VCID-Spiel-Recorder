from app import app, db
from app.models import User, Partien, Spiele, Teilnehmer

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Partien': Partien, 'Spiele': Spiele, 'Teilnehmer': Teilnehmer}
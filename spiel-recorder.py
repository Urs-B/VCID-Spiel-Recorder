from app import app, db
from app.models import User, Partien, Spiele, Teilnehmer

# Diese Methode stellt eine Flask Shell zur verfügung und wurde aus den Unterrichtsunterlagen übernommen
# Quelle: Jochen Reinholdt, Webapplikationen mit Flask
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Partien': Partien, 'Spiele': Spiele, 'Teilnehmer': Teilnehmer}
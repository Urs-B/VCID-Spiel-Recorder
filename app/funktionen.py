from app import db
from app.models import Teilnehmer

def add_teilnehmer(partie_id, *teilnehmer_ids):
    for teilnehmer_id in teilnehmer_ids:
        teilnehmer = Teilnehmer(partie_id=partie_id, user_id=teilnehmer_id)
        db.session.add(teilnehmer)
    db.session.commit()
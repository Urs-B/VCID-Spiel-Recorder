from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Klasse für das DB Model für User, Übernommen aus den Unterrichtsunterlagen
# Quelle: Jochen Reinholdt, Webapplikationen mit Flask
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    passwort_hash = db.Column(db.String(128))
    lieblingsspiel_id = db.Column(db.Integer, db.ForeignKey('spiele.spiel_id'))

    lieblingsspiel = db.relationship('Spiele')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.passwort_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.passwort_hash, password)
    
    def to_dict(self):
        spiel = self.lieblingsspiel.spielname if self.lieblingsspiel else "Kein Lieblingsspiel ausgewählt"
        data = {
            'id': self.id,
            'Username': self.username,
            'Email': self.email,
            'Lieblingsspiel': spiel
        }
        return data
    
    @staticmethod
    def to_collection():
        users = User.query.all()
        data = {'items': [item.to_dict() for item in users]}
        return data

# Methode für Userhandling, Übernommen aus den Unterrichtsunterlagen
# Quelle: Jochen Reinholdt, Webapplikationen mit Flask
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Klasse für das DB Model für Spiele
class Spiele(db.Model):
    spiel_id = db.Column(db.Integer, primary_key=True)
    spielname = db.Column(db.String(64), index=True, unique=True)
    spieler_min = db.Column(db.Integer)
    spieler_max = db.Column(db.Integer)
    dauer_min = db.Column(db.Integer)
    dauer_max = db.Column(db.Integer)

    def __repr__(self):
        return '<Spiel {}>'.format(self.spielname)

# Methode um ein Spiel für die API aufzubereiten
    def to_dict(self):
        data = {
            'id': self.spiel_id,
            'Spielname': self.spielname,
            'Spieleranzahl': str(self.spieler_min) + " bis " + str(self.spieler_max),
            'Spieldauer': str(self.dauer_min) + " bis " + str(self.dauer_max) + " Minuten"
        }
        return data

# Methode um alle Spiele für die API aufzubereiten
    @staticmethod
    def to_collection():
        spiele = Spiele.query.all()
        data = {'items': [item.to_dict() for item in spiele]}
        return data

# Klasse für das DB Model für Spiele
class Partien(db.Model):
    partie_id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.Date)
    spiel_id = db.Column(db.Integer, db.ForeignKey('spiele.spiel_id'))
    gewinner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Definiert die Beziehungen zu den anderen Klassen
    spiel = db.relationship('Spiele')
    gewinner = db.relationship('User', backref='gewonnene_partien')
    teilnehmer = db.relationship('User', secondary='teilnehmer', backref='teilgenommen_partien')

# Methode um eine Partie für die API aufzubereiten
    def to_dict(self):
        # Die Namen der Teilnehmer werden zu einem String verknüpft und in eine Variable überführt
        teilnehmer_string = ", ".join([teilnehmer.username for teilnehmer in self.teilnehmer])
        data = {
            'id': self.partie_id,
            'Datum': self.datum,
            'Spiel': self.spiel.spielname,
            'Gewinner': self.gewinner.username,
            'Teilnehmer': teilnehmer_string
        }
        return data
# Methode um alle Spiele für die API aufzubereiten
    @staticmethod
    def to_collection():
        partien = Partien.query.all()
        data = {'items': [item.to_dict() for item in partien]}
        return data

# Klasse für das DB Model für die Teilnehmer.
# Eine Hilfsklasse, die Partien und User miteinander verknüpft.
class Teilnehmer(db.Model):
    teilnahme_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    partie_id = db.Column(db.Integer, db.ForeignKey('partien.partie_id'))
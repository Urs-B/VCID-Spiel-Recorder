from datetime import datetime
from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    passwort_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Spiele(db.Model):
    spiel_id = db.Column(db.Integer, primary_key=True)
    spielname = db.Column(db.String(64), index=True, unique=True)
    spieler_min = db.Column(db.Integer)
    spieler_max = db.Column(db.Integer)
    dauer_min = db.Column(db.Integer)
    dauer_max = db.Column(db.Integer)

    def __repr__(self):
        return '<Spiel {}>'.format(self.spielname)

class Partien(db.Model):
    partie_id = db.Column(db.Integer, primary_key=True)

class Teilnehmer(db.Model):
    teilnahme_id = db.Column(db.Integer, primary_key=True)
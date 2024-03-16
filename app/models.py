from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    passwort_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.passwort_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.passwort_hash, password)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

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
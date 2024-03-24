from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from app.models import User, Spiele

# Formularklasse für das Login, Übernommen aus den Unterrichtsunterlagen
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# Formularklasse für das Registrieren neuer User, Übernommen aus den Unterrichtsunterlagen
class RegisterForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Bitte einen anderen Benutzernamen verwenden.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Bitte eine andere Email Adresse verwenden.')

# Formularklasse für das Editieren von Benutzerdaten
class EditUserForm(FlaskForm):
    username = StringField('Benutzername')
    lieblingsspiel = SelectField('Lieblingsspiel', coerce=int)
    submit = SubmitField('Ändern')

# Formularklasse für das Erfassen von neuen Spielen
class SpieleForm(FlaskForm):
    spielname = StringField('Spielname', validators=[DataRequired()])
    dauer_min = IntegerField('Minimaldauer in Minuten', validators=[DataRequired(), NumberRange(1,1000)])
    dauer_max = IntegerField('Maximaldauer in Minuten', validators=[DataRequired(), NumberRange(1,1000)])
    spieler_min = IntegerField('Spieler minimum', validators=[DataRequired(), NumberRange(1,6)])
    spieler_max = IntegerField('Spieler maximum', validators=[DataRequired(), NumberRange(1,6)])
    submit = SubmitField('Erfassen')

    def validate_spielname(self, spielname):
        spiel = Spiele.query.filter_by(spielname=spielname.data).first()
        if spiel is not None:
            raise ValidationError('Spiel ist bereits in der Sammlung.')

# Formularklasse für das Erfassen einer gespielten Partie
class PartienForm(FlaskForm):
    datum = DateField('Datum der Partie (Format Jahr-Monat-Tag)', format='%Y-%m-%d', validators=[DataRequired()])
    spiel = SelectField('Gespieltes Spiel', coerce=int)
    gewinner = SelectField('Gewinner der Partie', coerce=int)
    mitspieler = IntegerField('Anzahl Mitspieler', validators=[DataRequired()])
    submit = SubmitField('Erfassen')

    def validate_mitspieler(self, mitspieler):
        aktuelles_spiel = Spiele.query.filter_by(spiel_id=self.spiel.data).first()
        max = aktuelles_spiel.spieler_max
        if mitspieler.data > max:
            raise ValidationError('Spiel nicht für so viele Mitspieler geeignet')

# Formularklassen Teilnehmer 2 - 6 sind für das Erfassen der Teilnehmer einer Partie
class Teilnehmer2Form(FlaskForm):
    teilnehmer1 = SelectField('Teilnehmer 1', coerce=int)
    teilnehmer2 = SelectField('Teilnehmer 2', coerce=int)
    submit = SubmitField('Erfassen')

class Teilnehmer3Form(FlaskForm):
    teilnehmer1 = SelectField('Teilnehmer 1', coerce=int)
    teilnehmer2 = SelectField('Teilnehmer 2', coerce=int)
    teilnehmer3 = SelectField('Teilnehmer 3', coerce=int)
    submit = SubmitField('Erfassen')

class Teilnehmer4Form(FlaskForm):
    teilnehmer1 = SelectField('Teilnehmer 1', coerce=int)
    teilnehmer2 = SelectField('Teilnehmer 2', coerce=int)
    teilnehmer3 = SelectField('Teilnehmer 3', coerce=int)
    teilnehmer4 = SelectField('Teilnehmer 4', coerce=int)
    submit = SubmitField('Erfassen')

class Teilnehmer5Form(FlaskForm):
    teilnehmer1 = SelectField('Teilnehmer 1', coerce=int)
    teilnehmer2 = SelectField('Teilnehmer 2', coerce=int)
    teilnehmer3 = SelectField('Teilnehmer 3', coerce=int)
    teilnehmer4 = SelectField('Teilnehmer 4', coerce=int)
    teilnehmer5 = SelectField('Teilnehmer 5', coerce=int)
    submit = SubmitField('Erfassen')

class Teilnehmer6Form(FlaskForm):
    teilnehmer1 = SelectField('Teilnehmer 1', coerce=int)
    teilnehmer2 = SelectField('Teilnehmer 2', coerce=int)
    teilnehmer3 = SelectField('Teilnehmer 3', coerce=int)
    teilnehmer4 = SelectField('Teilnehmer 4', coerce=int)
    teilnehmer5 = SelectField('Teilnehmer 5', coerce=int)
    teilnehmer6 = SelectField('Teilnehmer 6', coerce=int)
    submit = SubmitField('Erfassen')
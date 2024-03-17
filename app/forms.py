from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from app.models import User, Spiele

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

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

class SpieleForm(FlaskForm):
    spielname = StringField('Spielname', validators=[DataRequired()])
    dauer_min = IntegerField('Minimaldauer in Minuten', validators=[DataRequired(), NumberRange(1,1000)])
    dauer_max = IntegerField('Maximaldauer in Minuten', validators=[DataRequired(), NumberRange(1,1000)])
    spieler_min = IntegerField('Spieler minimum', validators=[DataRequired(), NumberRange(1,10)])
    spieler_max = IntegerField('Spieler maximum', validators=[DataRequired(), NumberRange(1,10)])
    submit = SubmitField('Erfassen')

    def validate_spielname(self, spielname):
        spiel = Spiele.query.filter_by(spielname=spielname.data).first()
        if spiel is not None:
            raise ValidationError('Spiel ist bereits in der Sammlung.')
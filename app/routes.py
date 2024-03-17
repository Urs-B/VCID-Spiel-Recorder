from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegisterForm, SpieleForm
from app.models import User, Partien, Spiele, Teilnehmer
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ungültiger Benutzername oder Passwort!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/registrieren', methods=['GET', 'POST'])
def registrieren():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Benutzer {} ist jetzt Registriert'.format(form.username.data))
        return redirect(url_for('login'))
    return render_template('registrieren.html', title='Registrierung', form=form)

@app.route('/spiele_anzeigen')
@login_required
def spiele_anzeigen():
    spiele = Spiele.query.all()
    return render_template('spiele_anzeigen.html', title='Spiele anzeigen', spiele=spiele)

@app.route('/spiele_erfassen', methods=['GET', 'POST'])
@login_required
def spiele_erfassen():
    form = SpieleForm()
    if form.validate_on_submit():
        spiel = Spiele(spielname=form.spielname.data, spieler_min=form.spieler_min.data, 
                       spieler_max=form.spieler_max.data, dauer_min=form.dauer_min.data,
                       dauer_max=form.dauer_max.data)
        db.session.add(spiel)
        db.session.commit()
        flash('Spiel {} wurde erfasst.'.format(form.spielname.data))
        return redirect(url_for('spiele_erfassen'))
    return render_template('spiele_erfassen.html', title='Spiele erfassen', form=form)

@app.route('/partien_anzeigen')
@login_required
def partien_anzeigen():
    return render_template('partien_anzeigen.html', titel='Partien anzeigen')

@app.route('/partien_erfassen')
@login_required
def partien_erfassen():
    return render_template('partien_erfassen.html', titel='Partien erfassen')



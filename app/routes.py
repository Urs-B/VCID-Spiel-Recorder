from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Anmeldung für Benutzer {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

@app.route('/registrieren', methods=['GET', 'POST'])
def registrieren():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Registrierung für Benutzer {}'.format(form.username.data))
        return redirect(url_for('index'))
    return render_template('registrieren.html', title='Registrierung', form=form)

@app.route('/spiele')
def spiele():
    return render_template('spiele.html', title='Spiele')

@app.route('/partien')
def partien():
    return render_template('partien.html', titel='Partien')
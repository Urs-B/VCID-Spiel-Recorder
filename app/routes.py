from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegisterForm, SpieleForm, EditUserForm, PartienForm, Teilnehmer4Form, \
     Teilnehmer2Form, Teilnehmer5Form, Teilnehmer6Form, Teilnehmer3Form
from app.models import User, Partien, Spiele, Teilnehmer
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.funktionen import add_teilnehmer

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

###################### Routen für Usermanagement ############################

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

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/profil_editieren', methods=['GET', 'POST'])
@login_required
def profil_editieren():
    form = EditUserForm()
    form.lieblingsspiel.choices = [(s.spiel_id, s.spielname) for s in Spiele.query.order_by('spielname')]
    if form.validate_on_submit():
        if form.username.data:
            current_user.username = form.username.data
        current_user.lieblingsspiel_id=form.lieblingsspiel.data
        db.session.commit()
        flash('Profil wurde angepasst')
        return redirect(url_for('profil_editieren'))
    return render_template('profil_editieren.html', title='Profil editieren', form=form)


###################### Routen für Spielemanagement ############################

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


###################### Routen für Management der Partien ############################

@app.route('/partien_anzeigen')
@login_required
def partien_anzeigen():
    return render_template('partien_anzeigen.html', titel='Partien anzeigen')

@app.route('/partien_erfassen', methods=['GET', 'POST'])
@login_required
def partien_erfassen():
    form = PartienForm()
    form.gewinner.choices = [(g.id, g.username) for g in User.query.order_by('username')]
    form.spiel.choices = [(s.spiel_id, s.spielname) for s in Spiele.query.order_by('spielname')]
    if form.validate_on_submit():
        partie = Partien(datum=form.datum.data, spiel_id=form.spiel.data, gewinner_id=form.gewinner.data)
        anzahl_spieler = form.mitspieler.data
        db.session.add(partie)
        db.session.commit()
        return redirect(url_for('teilnehmer_erfassen', anzahl=anzahl_spieler))
    return render_template('partien_erfassen.html', titel='Partien erfassen', form=form)

@app.route('/teilnehmer_erfassen/<anzahl>', methods=['GET', 'POST'])
@login_required
def teilnehmer_erfassen(anzahl):
    if anzahl == "2":
        form = Teilnehmer2Form()
        form.teilnehmer1.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer2.choices = [(g.id, g.username) for g in User.query.order_by('username')]
    elif anzahl == "3":
        form = Teilnehmer3Form()
        form.teilnehmer1.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer2.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer3.choices = [(g.id, g.username) for g in User.query.order_by('username')]
    elif anzahl == "4":
        form = Teilnehmer4Form()
        form.teilnehmer1.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer2.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer3.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer4.choices = [(g.id, g.username) for g in User.query.order_by('username')]
    elif anzahl == "5":
        form = Teilnehmer5Form()
        form.teilnehmer1.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer2.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer3.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer4.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer5.choices = [(g.id, g.username) for g in User.query.order_by('username')]
    elif anzahl == "6":
        form = Teilnehmer6Form()
        form.teilnehmer1.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer2.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer3.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer4.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer5.choices = [(g.id, g.username) for g in User.query.order_by('username')]
        form.teilnehmer5.choices = [(g.id, g.username) for g in User.query.order_by('username')]
    else:
        return render_template('index.html')
    partie = Partien.query.order_by(Partien.partie_id.desc()).first()
    partie_id = partie.partie_id
    if form.validate_on_submit():
        if anzahl == "2":
            add_teilnehmer(partie_id, form.teilnehmer1.data, form.teilnehmer2.data)
            flash('Teilnehmer erfasst')
            return redirect(url_for('index'))
        elif anzahl == "3":
            add_teilnehmer(partie_id, form.teilnehmer1.data, form.teilnehmer2.data, form.teilnehmer3.data)
            flash('Teilnehmer erfasst')
            return redirect(url_for('index'))
        elif anzahl == "4":
            add_teilnehmer(partie_id, form.teilnehmer1.data, form.teilnehmer2.data, form.teilnehmer3.data, form.teilnehmer4.data)
            flash('Teilnehmer erfasst')
            return redirect(url_for('index'))
        elif anzahl == "5":
            add_teilnehmer(partie_id, form.teilnehmer1.data, form.teilnehmer2.data, form.teilnehmer3.data, form.teilnehmer4.data,
                           form.teilnehmer5.data)
            flash('Teilnehmer erfasst')
            return redirect(url_for('index'))
        elif anzahl == "6":
            add_teilnehmer(partie_id, form.teilnehmer1.data, form.teilnehmer2.data, form.teilnehmer3.data, form.teilnehmer4.data,
                           form.teilnehmer5.data, form.teilnehmer6.data)
            flash('Teilnehmer erfasst')
            return redirect(url_for('index'))
    return render_template('teilnehmer_erfassen.html', titel='Teilnehmer erfassen', form=form)


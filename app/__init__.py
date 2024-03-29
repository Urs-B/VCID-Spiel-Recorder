# Diese Datei wurde aus den Unterrichtsunterlagen übernommen
# Quelle: Jochen Reinholdt, Webapplikationen mit Flask
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, api
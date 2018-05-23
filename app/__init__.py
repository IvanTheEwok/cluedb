#Imports
from flask import Flask, current_app
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from config import Config

#Create variable for extensions
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Please log in to access this page."
moment = Moment()

#Application factory
def create_app(config_class=Config):
    #Creates the flask app and loads config variables from the config file
    app = Flask(__name__)
    app.config.from_object(config_class)

    #Initiate extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login.init_app(app)
    moment.init_app(app)

    #Import blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models
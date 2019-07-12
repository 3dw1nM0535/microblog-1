from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy()
migrate=Migrate()
mail=Mail()
bootstrap=Bootstrap()
moment=Moment()

login=LoginManager(app)
login.login_view='auth.login'

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.errors import BP as error_blueprint
    app.register_blueprint(error_blueprint)

    from app.auth import BP as authentication_blueprint
    app.register_blueprint(authentication_blueprint, url_prefix='/auth')

    from app.main import BP as microblog_blueprint
    app.register_blueprint(microblog_blueprint)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth=None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure=None
            if app.config['MAIL_USE_TLS']:
                secure=()
            mail_handler=SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler=RotatingFileHandler(
            'logs/microblog.log',
            maxBytes=10240,
            backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app

from app import models

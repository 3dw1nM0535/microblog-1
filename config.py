# Configuration variable
import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-ever-guess'
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    MAIL_SERVER=os.environ.get('MAIL_SERVER')
    MAIL_PORT=os.environ.get('MAIL_PORT')
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    MAIL_USE_SSL=False
    ADMINS=['email@example.com']
    POSTS_PER_PAGE=25
    SECRET=os.environ.get('SECRET')
    ELASTICSEARCH_URL=os.environ.get('ELASTICSEARCH_URL')

from flask import Blueprint

BP=Blueprint('microblog', __name__)

from app.microblog import routes

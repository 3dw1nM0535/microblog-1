from flask import Blueprint

BP=Blueprint('auth', __name__)

from app.auth import routes

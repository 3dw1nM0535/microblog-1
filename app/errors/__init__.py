from flask import Blueprint

BP=Blueprint('errors', __name__)

from app.errors import handlers

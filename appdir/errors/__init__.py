from flask import Blueprint

bp = Blueprint('errors', __name__)

from appdir.errors import handlers
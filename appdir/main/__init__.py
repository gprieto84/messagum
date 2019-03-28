from flask import Blueprint

bp = Blueprint('main', __name__)

from appdir.main import routes
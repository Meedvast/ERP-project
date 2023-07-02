from flask.blueprints import Blueprint
manager_bp = Blueprint('manager', __name__, url_prefix='/api/manager')
from backend.service.manager import view


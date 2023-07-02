from flask.blueprints import Blueprint
inrecord_bp = Blueprint('inrecord', __name__, url_prefix='/api/inrecord')
outrecord_bp = Blueprint('outrecord', __name__, url_prefix='/api/outrecord')
from backend.service.record import view

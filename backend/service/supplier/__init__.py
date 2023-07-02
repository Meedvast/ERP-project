from flask.blueprints import Blueprint
supplier_bp = Blueprint('supplier', __name__, url_prefix='/api/supplier')
from backend.service.supplier import view


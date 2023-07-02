from flask.blueprints import Blueprint
inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')
from backend.service.inventory import view

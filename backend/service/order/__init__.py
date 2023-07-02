from flask.blueprints import Blueprint
order_bp = Blueprint('order', __name__, url_prefix='/api/order')
from backend.service.order import view


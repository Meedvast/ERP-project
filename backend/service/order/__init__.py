from flask.blueprints import Blueprint
order_bp = Blueprint('order', __name__, url_prefix='/api/')
order_detail_bp = Blueprint('order_detail', __name__, url_prefix='/api/')
from backend.service.order import view


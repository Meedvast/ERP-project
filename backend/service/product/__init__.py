from flask.blueprints import Blueprint
product_bp = Blueprint('product', __name__, url_prefix='/api/product')
from backend.service.product import view


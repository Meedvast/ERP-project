from flask.blueprints import Blueprint
customer_bp = Blueprint('customer', __name__, url_prefix='/api/customer')
from backend.service.customer import view


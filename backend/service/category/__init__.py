from flask.blueprints import Blueprint
category_bp = Blueprint('category', __name__, url_prefix='/api/category')
from backend.service.category import view

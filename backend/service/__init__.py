from backend.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# 定义database
db = SQLAlchemy()


def create_app(model='base'):
    app = Flask(__name__)
    CORS(app, resources=r'/*')
    obj = config.get(model)
    app.config.from_object(obj)
    db.init_app(app)
    Migrate(app, db)

    # 注册蓝图
    from backend.service.manager import manager_bp
    app.register_blueprint(manager_bp)
    from backend.service.order import order_bp, order_detail_bp
    app.register_blueprint(order_bp)
    app.register_blueprint(order_detail_bp)
    from backend.service.customer import customer_bp
    app.register_blueprint(customer_bp)
    from backend.service.product import product_bp
    app.register_blueprint(product_bp)
    from backend.service.category import category_bp
    app.register_blueprint(category_bp)
    from backend.service.supplier import supplier_bp
    app.register_blueprint(supplier_bp)
    from backend.service.record import inrecord_bp, outrecord_bp
    app.register_blueprint(inrecord_bp)
    app.register_blueprint(outrecord_bp)
    from backend.service.inventory import inventory_bp
    app.register_blueprint(inventory_bp)

    return app

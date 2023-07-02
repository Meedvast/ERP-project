from backend.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 定义database
db = SQLAlchemy()


def create_app(model='base'):
    app = Flask(__name__)
    obj = config.get(model)
    app.config.from_object(obj)
    db.init_app(app)
    Migrate(app, db)

    # 注册蓝图
    from backend.service.manager import manager_bp
    app.register_blueprint(manager_bp)
    from backend.service import test_bp
    app.register_blueprint(test_bp)
    return app


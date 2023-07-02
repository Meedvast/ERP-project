class BaseConfig:
    # 数据库
    HOST = '127.0.0.1'
    PORT = 3306
    DATABASE = 'ERP'
    USER = 'root'
    PWD = '123456'
    DB_URI = f'mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 密钥
    SECRET_KEY = '123456'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
    'base': BaseConfig
}

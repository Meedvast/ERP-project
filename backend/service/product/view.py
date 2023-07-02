from flask import request
from backend.service.models import Product
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.product import product_bp


class ProductView(Resource):
    # 获取产品信息，当没有参数传入时获取全部产品，当有产品pid传入时获取该产品信息
    def get(self, msg=None):
        try:
            pid = request.args.get('pid')
            if pid:
                product = Product.query.filter_by(pid=pid).first()
                if product:
                    return to_dict_msg(200, data=product.to_dict())
                else:
                    return to_dict_msg(200, msg='产品不存在')
            else:
                products = Product.query.all()
                return to_dict_msg(200, data=[product.to_dict() for product in products])
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    # 添加产品
    def post(self):
        pid = request.json.get('pid')
        name = request.json.get('name')
        type = request.json.get('type')
        unit = request.json.get('unit')
        sid = request.json.get('sid')
        category = request.json.get('category')
        if not all([pid, name, type, unit, sid, category]):
            return to_dict_msg(400, msg='请输入完整信息')
        if Product.query.filter(Product.pid == pid, Product.name == name, Product.type == type, ).all():
            return to_dict_msg(400, msg='产品已存在')
        else:
            try:
                product = Product(pid=pid, name=name, type=type, unit=unit, sid=sid, category=category)
                db.session.add(product)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    # 修改订单
    def put(self):
        pid = request.json.get('pid')
        name = request.json.get('name')
        type = request.json.get('type')
        unit = request.json.get('unit')
        sid = request.json.get('sid')
        category = request.json.get('category')
        if not all([pid, name, type, unit, sid, category]):
            return to_dict_msg(400, msg='请输入完整信息')
        product = Product.query.filter_by(pid=pid).first()
        if product:
            try:
                product.pid = pid,
                product.name = name,
                product.type = type,
                product.unit = unit,
                product.sid = sid,
                product.category = category,
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='产品不存在')

    # 删除产品
    def delete(self):
        pid = request.json.get('pid')
        product = Product.query.filter_by(pid=pid).first()
        if product:
            try:
                db.session.delete(product)
                db.session.commit()
                return to_dict_msg(200, msg='删除成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='产品不存在')

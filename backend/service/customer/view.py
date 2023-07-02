from flask import request
from backend.service.models import Customer
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.order import customer_bp


class CustomerView(Resource):
    # 获取客户信息，当没有参数传入时获取全部客户，当有客户id传入时获取该客户信息
    def get(self, msg=None):
        try:
            id = request.args.get('id')
            if id:
                customer = Customer.query.filter_by(id=id).first()
                if customer:
                    return to_dict_msg(200, data=customer.to_dict())
                else:
                    return to_dict_msg(200, msg='客户不存在')
            else:
                customers = Customer.query.all()
                return to_dict_msg(200, data=[customer.to_dict() for customer in customers])
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    # 添加客户
    def post(self):
        id = request.json.get('id')
        name = request.json.get('name')
        address = request.json.get('address')
        phone = request.json.get('phone')
        email = request.json.get('email')
        remark = request.json.get('remark')
        if not all([id, name, address, phone, email, remark]):
            return to_dict_msg(400, msg='请输入完整信息')
        if Customer.query.filter(Customer.id == id, Customer.name == name, Customer.address == address,
                                 Customer.phone == phone, Customer.email == email, Customer.remark == remark).all():
            return to_dict_msg(400, msg='客户已存在')
        else:
            try:
                customer = Customer(id=id, name=name, address=address, phone=phone, email=email, remark=remark)
                db.session.add(customer)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    # 修改客户信息
    def put(self):
        id = request.json.get('id')
        name = request.json.get('name')
        address = request.json.get('address')
        phone = request.json.get('phone')
        email = request.json.get('email')
        remark = request.json.get('remark')
        if not all([id, name, address, phone, email, remark]):
            return to_dict_msg(400, msg='请输入完整信息')
        customer = Customer.query.filter_by(id=id).first()
        if customer:
            try:
                customer.id = id
                customer.name = name
                customer.address = address
                customer.phone = phone
                customer.email = email
                customer.remark = remark
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='客户不存在')

    # 删除客户信息
    def delete(self):
        id = request.json.get('id')
        customer = Customer.query.filter_by(id=id).first()
        if customer:
            try:
                db.session.delete(customer)
                db.session.commit()
                return to_dict_msg(200, msg='删除成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='客户不存在')
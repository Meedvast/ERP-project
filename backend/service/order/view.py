from flask import request
from backend.service.models import Order
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.order import order_bp

class OrderView(Resource):
    # 获取订单信息，当没有参数传入时获取全部订单，当有订单id传入时获取该订单信息
    def get(self, msg=None):
        try:
            id = request.args.get('id')
            if id:
                order = Order.query.filter_by(id=id).first()
                if order:
                    return to_dict_msg(200, data=order.to_dict())
                else:
                    return to_dict_msg(200, msg='订单不存在')
            else:
                orders = Order.query.all()
                return to_dict_msg(200, data=[order.to_dict() for order in orders])
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    # 添加订单
    def post(self):
        sid = request.json.get('sid')
        cid = request.json.get('cid')
        pid = request.json.get('pid')
        price = request.json.get('price')
        amount = request.json.get('amount')
        money = request.json.get('money')
        book_time = request.json.get('book_time')
        order_time = request.json.get('order_time')
        remark = request.json.get('remark')
        if not all([sid, cid, pid, price, amount, money, book_time, order_time]):
            return to_dict_msg(400, msg='请输入完整信息')
        if Order.query.filter(Order.sid == sid, Order.cid == cid, Order.pid == pid, Order.price == price, Order.amount == amount, Order.money == money, Order.book_time == book_time, Order.order_time == order_time, Order.remark == remark).all():
            return to_dict_msg(400, msg='订单已存在')
        else:
            try:
                order = Order(sid=sid, cid=cid, pid=pid, price=price, amount=amount, money=money, book_time=book_time, order_time=order_time, remark=remark)
                db.session.add(order)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    # 修改订单
    def put(self):
        oid = request.json.get('oid')
        sid = request.json.get('sid')
        cid = request.json.get('cid')
        pid = request.json.get('pid')
        price = request.json.get('price')
        amount = request.json.get('amount')
        money = request.json.get('money')
        book_time = request.json.get('book_time')
        order_time = request.json.get('order_time')
        remark = request.json.get('remark')
        if not all([oid, sid, cid, pid, price, amount, money, book_time, order_time]):
            return to_dict_msg(400, msg='请输入完整信息')
        order = Order.query.filter_by(oid=oid).first()
        if order:
            try:
                order.sid = sid
                order.cid = cid
                order.pid = pid
                order.price = price
                order.amount = amount
                order.money = money
                order.book_time = book_time
                order.order_time = order_time
                order.remark = remark
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='订单不存在')

    # 删除订单
    def delete(self):
        id = request.json.get('id')
        order = Order.query.filter_by(id=id).first()
        if order:
            try:
                db.session.delete(order)
                db.session.commit()
                return to_dict_msg(200, msg='删除成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='订单不存在')


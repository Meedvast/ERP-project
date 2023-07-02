from flask import request
from backend.service.models import Order, Order_detail
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.order import order_bp, order_detail_bp

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


# 订单处理明细
class Order_detailView(Resource):
    # 获取订单处理明细，当没有参数传入时获取全部订单处理明细，当有订单id传入时获取该订单处理明细
    def get(self, msg=None):
        try:
            id = request.args.get('id')
            if id:
                order_detail = Order.query.filter_by(id=id).first()
                if order_detail:
                    return to_dict_msg(200, data=order_detail.to_dict())
                else:
                    return to_dict_msg(200, msg='订单处理明细不存在')
            else:
                order_details = Order_detail.query.all()
                return to_dict_msg(200, data=[order_detail.to_dict() for order_detail in order_details])
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    # 添加订单处理明细
    def post(self):
        id = request.json.get('id')
        sid = request.json.get('sid')
        cid = request.json.get('cid')
        pid = request.json.get('pid')
        price = request.json.get('price')
        amount = request.json.get('amount')
        money = request.json.get('money')
        book_time = request.json.get('book_time')
        order_time = request.json.get('order_time')
        method = request.json.get('method')
        pay_time = request.json.get('pay_time')
        address = request.json.get('address')
        person = request.json.get('person')
        state = request.json.get('state')
        if not all([id, cid, pid, sid, book_time, order_time, price, amount, money, method, pay_time, address, person, state]):
            return to_dict_msg(400, msg='请输入完整信息')
        if Order_detail.query.filter(Order_detail.id == id, Order_detail.sid == sid, Order_detail.cid == cid,
                                     Order_detail.pid == pid, Order_detail.price == price, Order_detail.amount == amount,
                                     Order_detail.money == money, Order_detail.book_time == book_time,
                                     Order_detail.order_time == order_time, Order_detail.method == method,
                                     Order_detail.pay_time == pay_time, Order_detail.address == address,
                                     Order_detail.person == person, Order_detail.state == state).all():
            return to_dict_msg(400, msg='订单处理明细已存在')
        else:
            try:
                order_detail = Order_detail(id=id, cid=cid, pid=pid, sid=sid, book_time=book_time, order_time=order_time,
                                            price=price, amount=amount, money=money, method=method, pay_time=pay_time,
                                            address=address, person=person, state=state)
                db.session.add(order_detail)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    # 修改订单
    def put(self):
        id = request.json.get('id')
        sid = request.json.get('sid')
        cid = request.json.get('cid')
        pid = request.json.get('pid')
        price = request.json.get('price')
        amount = request.json.get('amount')
        money = request.json.get('money')
        book_time = request.json.get('book_time')
        order_time = request.json.get('order_time')
        method = request.json.get('method')
        pay_time = request.json.get('pay_time')
        address = request.json.get('address')
        person = request.json.get('person')
        state = request.json.get('state')
        if not all([id, cid, pid, sid, book_time, order_time, price, amount, money, method, pay_time, address, person,
                    state]):
            return to_dict_msg(400, msg='请输入完整信息')
        order_detail = Order_detail.query.filter_by(id=id).first()
        if order_detail:
            try:
                order_detail.id = id,
                order_detail.cid = cid,
                order_detail.pid = pid,
                order_detail.sid = sid,
                order_detail.book_time = book_time,
                order_detail.order_time = order_time,
                order_detail.price = price,
                order_detail.amount = amount,
                order_detail.money = money,
                order_detail.pay_time = pay_time,
                order_detail.address = address,
                order_detail.person = person,
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='订单处理明细不存在')

    # 删除订单处理明细
    def delete(self):
        id = request.json.get('id')
        order_detail = Order_detail.query.filter_by(id=id).first()
        if order_detail:
            try:
                db.session.delete(order_detail)
                db.session.commit()
                return to_dict_msg(200, msg='删除成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='订单处理明细不存在')
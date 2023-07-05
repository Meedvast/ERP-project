from flask import request
from backend.service.models import Order, Order_detail
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.order import order_bp, order_detail_bp


class OrderView(Resource):
    # 获取订单信息，当没有参数传入时获取全部订单，根据传入的参数获取对应订单

    def get(self, msg=None):
        try:
            id = request.args.get('id')
            sid = request.args.get('sid')
            cid = request.args.get('cid')
            pid = request.args.get('pid')

            filterlist = []
            if id != '' and id is not None:
                filterlist.append(Order.id == id)
            if sid != '' and sid is not None:
                filterlist.append(Order.sid == sid)
            if cid != '' and cid is not None:
                filterlist.append(Order.cid == cid)
            if pid != '' and pid is not None:
                filterlist.append(Order.pid == pid)
            if filterlist:
                order = Order.query.filter(*filterlist).all()
                if order:
                    return to_dict_msg(200, data=[order.to_dict() for order in order])
                else:
                    return to_dict_msg(200, msg='订单不存在')
            else:
                orders = Order.query.all()
                return to_dict_msg(200, data=[order.to_dict() for order in orders])

        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    # 添加订单
    def post(self):
        id = request.form.get('id')
        sid = request.form.get('sid')
        cid = request.form.get('cid')
        pid = request.form.get('pid')
        price = request.form.get('price')
        amount = request.form.get('amount')
        money = request.form.get('money')
        book_time = request.form.get('book_time')
        order_time = request.form.get('order_time')
        remark = request.form.get('remark')
        if not all([id, sid, cid, pid, price, amount, money, book_time, order_time]):
            return to_dict_msg(400, msg='请输入完整信息')
        if Order.query.filter_by(id=id).first():
            return to_dict_msg(400, msg='订单已存在')
        else:
            try:
                order = Order(id=id, sid=sid, cid=cid, pid=pid, price=price, amount=amount, money=money, book_time=book_time,
                              order_time=order_time, remark=remark)
                db.session.add(order)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    # 修改订单
    def put(self):
        oid = request.form.get('oid')
        sid = request.form.get('sid')
        cid = request.form.get('cid')
        pid = request.form.get('pid')
        price = request.form.get('price')
        amount = request.form.get('amount')
        money = request.form.get('money')
        book_time = request.form.get('book_time')
        order_time = request.form.get('order_time')
        remark = request.form.get('remark')
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
        id = request.args.get('id')
        order = Order.query.filter_by(id=id).first()
        Order_detail.query.filter_by(id=id).delete()
        if order:
            try:
                db.session.delete(order)
                db.session.delete(Order_detail)
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
                order_detail = Order_detail.query.filter_by(id=id).first()
                if order_detail:
                    return to_dict_msg(200, data=order_detail.to_dict())
                else:
                    return to_dict_msg(200, msg='订单处理明细不存在')
            else:
                order_details = Order_detail.query.all()
                return to_dict_msg(200, data=[order_detail.to_dict() for order_detail in order_details])
        except Exception as e:
            db.session.rollback()
            return to_dict_msg(500, msg=str(e))

    # 添加订单处理明细
    def post(self):
        id = request.form.get('id')
        sid = request.form.get('sid')
        cid = request.form.get('cid')
        pid = request.form.get('pid')
        price = request.form.get('price')
        amount = request.form.get('amount')
        money = request.form.get('money')
        book_time = request.form.get('book_time')
        order_time = request.form.get('order_time')
        method = request.form.get('method')
        pay_time = request.form.get('pay_time')
        address = request.form.get('address')
        person = request.form.get('person')
        state = request.form.get('state')
        remark = request.form.get('remark')
        if not all([id, cid, pid, sid, book_time, order_time, price, amount, money, method, pay_time, address, person,
                    state]):
            return to_dict_msg(400, msg='请输入完整信息')
        if Order_detail.query.filter_by(id=id).first():
            return to_dict_msg(400, msg='订单处理明细已存在')
        else:
            try:
                if remark:
                    order = Order(id=id, sid=sid, cid=cid, pid=pid, price=price, amount=amount, money=money,
                                  book_time=book_time,
                                  order_time=order_time, remark=remark)
                else:
                    order = Order(id=id, sid=sid, cid=cid, pid=pid, price=price, amount=amount, money=money,
                                  book_time=book_time,
                                  order_time=order_time, remark=None)
                order_detail = Order_detail(id=id, cid=cid, pid=pid, sid=sid, book_time=book_time,
                                            order_time=order_time,
                                            price=price, amount=amount, money=money, method=method, pay_time=pay_time,
                                            address=address, person=person, state=state)
                db.session.add(order)
                db.session.add(order_detail)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg='数据库错误')

    # 修改订单
    def put(self):
        id = request.form.get('id')
        sid = request.form.get('sid')
        cid = request.form.get('cid')
        pid = request.form.get('pid')
        price = request.form.get('price')
        amount = request.form.get('amount')
        money = request.form.get('money')
        book_time = request.form.get('book_time')
        order_time = request.form.get('order_time')
        method = request.form.get('method')
        pay_time = request.form.get('pay_time')
        address = request.form.get('address')
        person = request.form.get('person')
        state = request.form.get('state')
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
                order_detail.method = method,
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='订单处理明细不存在')

    # 删除订单处理明细
    def delete(self):
        id = request.args.get('id')
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


order_api = Api(order_bp)
order_api.add_resource(OrderView, '/order/', endpoint='order')
order_detail_api = Api(order_detail_bp)
order_detail_api.add_resource(Order_detailView, '/orderdetail/', endpoint='orderdetail')

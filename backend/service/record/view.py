from flask import request
from backend.service.models import Inrecord
from backend.service.models import Outrecord
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.record import inrecord_bp, outrecord_bp


# 入库记录
class InrecordView(Resource):
    # 获取入库记录，当没有参数传入时获取全部入库记录，当有入库id传入时获取该入库记录
    def get(self, msg=None):
        try:
            id = request.args.get('id')
            if id:
                inrecord = Inrecord.query.filter_by(id=id).first()
                if inrecord:
                    return to_dict_msg(200, data=inrecord.to_dict())
                else:
                    return to_dict_msg(200, msg='订单不存在')
            else:
                inrecords = Inrecord.query.all()
                return to_dict_msg(200, data=[inrecord.to_dict() for inrecord in inrecords])
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    # 添加入库记录
    def post(self):
        id = request.json.get('id')
        category = request.json.get('category')
        pid = request.json.get('pid')
        sid = request.json.get('sid')
        in_time = request.json.get('in_time')
        price = request.json.get('price')
        amount = request.json.get('amount')
        money = request.json.get('money')
        person = request.json.get('person')
        if not all([id, category, pid, sid, in_time, price, amount, money, person]):
            return to_dict_msg(400, msg='请输入完整信息')
        if Inrecord.query.filter(Inrecord.id == id, Inrecord.category == category, Inrecord.pid == pid,
                                 Inrecord.sid == sid, Inrecord.in_time == in_time, Inrecord.price == price,
                                 Inrecord.amount == amount, Inrecord.money == money, Inrecord.person == person).all():
            return to_dict_msg(400, msg='入库记录已存在')
        else:
            try:
                inrecord = Inrecord(id=id, category=category, pid=pid, sid=sid, in_time=in_time, price=price,
                                    amount=amount, money=money, person=person)
                db.session.add(inrecord)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    # 修改入库记录
    def put(self):
        id = request.json.get('id')
        category = request.json.get('category')
        pid = request.json.get('pid')
        sid = request.json.get('sid')
        in_time = request.json.get('in_time')
        price = request.json.get('price')
        amount = request.json.get('amount')
        money = request.json.get('money')
        person = request.json.get('person')
        if not all([id, category, pid, sid, in_time, price, amount, money, person]):
            return to_dict_msg(400, msg='请输入完整信息')
        inrecord = Inrecord.query.filter_by(id=id).first()
        if inrecord:
            try:
                inrecord.id = id,
                inrecord.category = category,
                inrecord.pid = pid,
                inrecord.sid = sid,
                inrecord.in_time = in_time,
                inrecord.price = price,
                inrecord.amount = amount,
                inrecord.money = money,
                inrecord.person = person,
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='入库记录不存在')

    # 删除入库记录
    def delete(self):
        id = request.json.get('id')
        inrecord = Inrecord.query.filter_by(id=id).first()
        if inrecord:
            try:
                db.session.delete(inrecord)
                db.session.commit()
                return to_dict_msg(200, msg='删除成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='入库记录不存在')


# 出库记录
class OutrecordView(Resource):
    # 获取出库记录，当没有参数传入时获取全部出库记录，当有出库id传入时获取该出库记录
    def get(self, msg=None):
        try:
            id = request.args.get('id')
            if id:
                outrecord = Outrecord.query.filter_by(id=id).first()
                if outrecord:
                    return to_dict_msg(200, data=outrecord.to_dict())
                else:
                    return to_dict_msg(200, msg='订单不存在')
            else:
                outrecords = Outrecord.query.all()
                return to_dict_msg(200, data=[outrecord.to_dict() for outrecord in outrecords])
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    # 添加出库记录
    def post(self):
        id = request.json.get('id')
        category = request.json.get('category')
        pid = request.json.get('pid')
        sid = request.json.get('sid')
        out_time = request.json.get('out_time')
        price = request.json.get('price')
        amount = request.json.get('amount')
        money = request.json.get('money')
        person = request.json.get('person')
        if not all([id, category, pid, sid, out_time, price, amount, money, person]):
            return to_dict_msg(400, msg='请输入完整信息')
        if Outrecord.query.filter(Outrecord.id == id, Outrecord.category == category, Outrecord.pid == pid,
                                  Outrecord.sid == sid, Outrecord.out_time == out_time, Outrecord.price == price,
                                  Outrecord.amount == amount, Outrecord.money == money,
                                  Outrecord.person == person).all():
            return to_dict_msg(400, msg='出库记录已存在')
        else:
            try:
                outrecord = Outrecord(id=id, category=category, pid=pid, sid=sid, out_time=out_time, price=price,
                                      amount=amount, money=money, person=person)
                db.session.add(outrecord)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    # 修改出库记录
    def put(self):
        id = request.json.get('id')
        category = request.json.get('category')
        pid = request.json.get('pid')
        sid = request.json.get('sid')
        out_time = request.json.get('out_time')
        price = request.json.get('price')
        amount = request.json.get('amount')
        money = request.json.get('money')
        person = request.json.get('person')
        if not all([id, category, pid, sid, out_time, price, amount, money, person]):
            return to_dict_msg(400, msg='请输入完整信息')
        outrecord = Outrecord.query.filter_by(id=id).first()
        if outrecord:
            try:
                outrecord.id = id,
                outrecord.category = category,
                outrecord.pid = pid,
                outrecord.sid = sid,
                outrecord.in_time = out_time,
                outrecord.price = price,
                outrecord.amount = amount,
                outrecord.money = money,
                outrecord.person = person,
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='出库记录不存在')

    # 删除入库记录
    def delete(self):
        id = request.json.get('id')
        outrecord = Outrecord.query.filter_by(id=id).first()
        if outrecord:
            try:
                db.session.delete(outrecord)
                db.session.commit()
                return to_dict_msg(200, msg='删除成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='出库记录不存在')

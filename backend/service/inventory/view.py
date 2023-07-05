from flask import request
from backend.service.models import Inventory
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.inventory import inventory_bp


class InventoryView(Resource):
    # 获取库存信息，当没有参数传入时获取全部库存，当有库存pid传入时获取该库存信息
    def get(self, msg=None):
        try:
            pid = request.args.get('pid')
            if pid:
                inventory = Inventory.query.filter_by(pid=pid).first()
                if inventory:
                    return to_dict_msg(200, data=inventory.to_dict())
                else:
                    return to_dict_msg(200, msg='库存不存在')
            else:
                inventories = Inventory.query.all()
                return to_dict_msg(200, data=[inventory.to_dict() for inventory in inventories])
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    # 添加库存
    def post(self):
        pid = request.form.get('pid')
        sid = request.form.get('sid')
        amount = request.form.get('amount')
        if not all([pid, sid, amount]):
            return to_dict_msg(400, msg='请输入完整信息')
        if Inventory.query.filter(Inventory.pid == pid, Inventory.sid == sid, Inventory.amount == amount).all():
            return to_dict_msg(400, msg='库存已存在')
        else:
            try:
                inventory = Inventory(pid=pid, sid=sid, amount=amount)
                db.session.add(inventory)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    # 修改库存
    def put(self):
        pid = request.form.get('pid')
        sid = request.form.get('sid')
        amount = request.form.get('amount')
        if not all([pid, sid, amount]):
            return to_dict_msg(400, msg='请输入完整信息')
        inventory = Inventory.query.filter_by(pid=pid).first()
        if inventory:
            try:
                inventory.pid = pid,
                inventory.sid = sid,
                inventory.amount = amount,
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='库存不存在')

    # 删除库存
    def delete(self):
        pid = request.args.get('pid')
        inventory = Inventory.query.filter_by(pid=pid).first()
        if inventory:
            try:
                db.session.delete(inventory)
                db.session.commit()
                return to_dict_msg(200, msg='删除成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='库存不存在')


inventory_api = Api(inventory_bp)
inventory_api.add_resource(InventoryView, '/', endpoint='inventory')

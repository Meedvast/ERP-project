from flask import request
from backend.service.models import Supplier
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.supplier import supplier_bp


class SupplierView(Resource):
    # 获取供应商信息，当没有参数传入时获取全部供应商，当有供应商id传入时获取该供应商信息
    def get(self, msg=None):
        try:
            sid = request.args.get('sid')
            cname = request.args.get('cname')
            filterlist = []
            if sid != '' and sid is not None:
                filterlist.append(Supplier.sid == sid)
            if cname != '' and cname is not None:
                filterlist.append(Supplier.cname == cname)
            if filterlist:
                supplier = Supplier.query.filter(*filterlist).first()
                if supplier:
                    return to_dict_msg(200, data=[supplier.to_dict() for supplier in supplier])
                else:
                    return to_dict_msg(200, data=None, msg='供应商不存在')
            else:
                suppliers = Supplier.query.all()
                return to_dict_msg(200, data=[supplier.to_dict() for supplier in suppliers])
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    # 添加供应商
    def post(self):
        sname = request.form.get('sname')
        cname = request.form.get('cname')
        cjob = request.form.get('cjob')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        remark = request.form.get('remark')
        if not all([sname, cname, cjob, address, phone, email, remark]):
            return to_dict_msg(400, msg='请输入供应商信息')
        if Supplier.query.filter(Supplier.sname == sname).all():
            return to_dict_msg(400, msg='供应商已存在')
        else:
            try:
                supplier = Supplier(sname=sname, cname=cname, address=address, cjob=cjob, phone=phone, email=email, remark=remark)
                db.session.add(supplier)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    # 修改供应商信息
    def put(self):
        sid = request.form.get('sid')
        sname = request.form.get('sname')
        cname = request.form.get('cname')
        cjob = request.form.get('cjob')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        remark = request.form.get('remark')
        if not all([sname, cname, cjob, address, phone, email, remark]):
            return to_dict_msg(400, msg='请输入供应商信息')
        supplier = Supplier.query.filter_by(sid=sid).first()
        if supplier:
            try:
                supplier.sname = sname
                supplier.cname = cname
                supplier.cjob = cjob
                supplier.address = address
                supplier.phone = phone
                supplier.email = email
                supplier.remark = remark
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='供应商不存在')

    # 删除供应商
    def delete(self):
        sid = request.args.get('sid')
        supplier = Supplier.query.filter_by(sid=sid).first()
        if supplier:
            try:
                db.session.delete(supplier)
                db.session.commit()
                return to_dict_msg(200, msg='删除成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='供应商不存在')


supplier_api = Api(supplier_bp)
supplier_api.add_resource(SupplierView, '/', endpoint='supplier')
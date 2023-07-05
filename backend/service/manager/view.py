from flask import request
from backend.service.models import Manager
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.manager import manager_bp


class LoginView(Resource):
    def get(self, msg=None):
        try:
            account = request.args.get('account')
            manager = Manager.query.filter_by(account=account).first()
            if manager:
                return to_dict_msg(200, data=account)
            else:
                return to_dict_msg(400, msg='用户不存在')
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    def post(self):
        account = request.args.get('account')
        password = request.args.get('password')
        if not all([account, password]):
            return to_dict_msg(400, msg='请输入用户名或密码')
        manager = Manager.query.filter_by(account=account).first()
        if manager:
            if manager.check_password(password):
                return to_dict_msg(200, msg='登录成功')
            else:
                return to_dict_msg(401, msg='密码错误')
        else:
            return to_dict_msg(400, msg='用户不存在')


class RegisterView(Resource):
    def post(self):
        account = request.json.get('account')
        pwd1 = request.json.get('password')
        pwd2 = request.json.get('password2')
        if not all([account, pwd1, pwd2]):
            return to_dict_msg(400, msg='请输入用户名或密码')
        if Manager.query.filter(Manager.account == account).all():
            return to_dict_msg(400, msg='用户名已存在')
        elif pwd1 != pwd2:
            return to_dict_msg(400, msg='两次密码不一致')
        else:
            try:
                manager = Manager(account=account, password=pwd1)
                db.session.add(manager)
                db.session.commit()
                return to_dict_msg(200, msg='注册成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    def put(self):
        try:
            account = request.json.get('account')
            manager = Manager.query.filter_by(account=account).first()
            if manager:
                manager.password = request.json.get('password')
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            else:
                return to_dict_msg(400, msg="数据库错误")
        except Exception as e:
            return to_dict_msg(500, msg=str(e))


manager_api = Api(manager_bp)
manager_api.add_resource(LoginView, '/login/', endpoint='login')
manager_api.add_resource(RegisterView, '/register/', endpoint='register')

from flask import request
from backend.service.models import Manager
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.manager import manager_bp


class LoginView(Resource):
    def get(self, msg=None):
        try:
            name = request.args.get('name')
            manager = Manager.query.filter_by(name=name).first()
            if manager:
                return to_dict_msg(200, data=manager.to_dict())
            else:
                return to_dict_msg(200, msg='用户不存在')
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    def post(self):
        # 修改密码
        name = request.json.get('name')
        password = request.json.get('password')
        if not all([name, password]):
            return to_dict_msg(400, msg='请输入用户名或密码')
        manager = Manager.query.filter_by(name=name).first()
        if manager:
            if manager.check_password(manager.password, password):
                return to_dict_msg(200, msg='登录成功')
            else:
                return to_dict_msg(400, msg='密码错误')


class RegisterView(Resource):
    def post(self):
        name = request.json.get('name')
        pwd1 = request.json.get('password')
        pwd2 = request.json.get('password2')
        if not all([name, pwd1, pwd2]):
            return to_dict_msg(400, msg='请输入用户名或密码')
        if Manager.query.filter(Manager.name == name).all():
            return to_dict_msg(400, msg='用户名已存在')
        elif pwd1 != pwd2:
            return to_dict_msg(400, msg='两次密码不一致')
        else:
            try:
                manager = Manager(name=name, password=pwd1)
                db.session.add(manager)
                db.session.commit()
                return to_dict_msg(200, msg='注册成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    def put(self):
        try:
            name = request.json.get('name')
            manager = Manager.query.filter_by(name=name).first()
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

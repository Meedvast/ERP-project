from flask import request
from backend.service.models import Category
from backend.service import db
from flask_restful import Resource, Api
from backend.service.utils.message import to_dict_msg

from backend.service.category import category_bp


class CategoryView(Resource):
    # 获取业务类别信息，当没有参数传入时获取全部业务类别，当有业务类别id传入时获取该业务类别信息
    def get(self, msg=None):
        try:
            category = request.args.get('category')
            if category:
                category = Category.query.filter_by(category=category).first()
                if category:
                    return to_dict_msg(200, data=category.to_dict())
                else:
                    return to_dict_msg(200, msg='业务类别不存在')
            else:
                categories = Category.query.all()
                return to_dict_msg(200, data=[category.to_dict() for category in categories])
        except Exception as e:
            return to_dict_msg(500, msg=str(e))

    # 添加业务类别
    def post(self):
        category = request.json.get('category')
        name = request.json.get('name')
        mark = request.json.get('mark')
        if not all([category, name, mark]):
            return to_dict_msg(400, msg='请输入完整信息')
        if Category.query.filter(Category.category == category, Category.name == name, Category.mark == mark).all():
            return to_dict_msg(400, msg='业务类别已存在')
        else:
            try:
                category = Category(category=category, name=name, mark=mark)
                db.session.add(category)
                db.session.commit()
                return to_dict_msg(200, msg='添加成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")

    # 修改业务类别
    def put(self):
        category = request.json.get('category')
        name = request.json.get('name')
        mark = request.json.get('mark')
        if not all([category, name, mark]):
            return to_dict_msg(400, msg='请输入完整信息')
        category = Category.query.filter_by(category=category).first()
        if category:
            try:
                category.category = category,
                category.name = name,
                category.mark = mark,
                db.session.commit()
                return to_dict_msg(200, msg='修改成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='业务类别不存在')

    # 删除业务类别
    def delete(self):
        category = request.json.get('category')
        category = Category.query.filter_by(category=category).first()
        if category:
            try:
                db.session.delete(category)
                db.session.commit()
                return to_dict_msg(200, msg='删除成功')
            except Exception:
                return to_dict_msg(500, msg="数据库错误")
        else:
            return to_dict_msg(400, msg='业务类别不存在')
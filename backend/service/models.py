from backend.service import db


class Category(db.Model):
    __tablename__ = 'category'
    category = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(20), nullable=False)
    mark = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<category %r>' % self.name

    def to_dict(self):
        return {
            'category': self.category,
            'name': self.name,
            'mark': self.mark
        }


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(18), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    remark = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<customer %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'remark': self.remark
        }


class Inrecord(db.Model):
    __tablename__ = 'inrecord'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    sid = db.Column(db.Integer, nullable=False)
    in_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    money = db.Column(db.DECIMAL(10, 2), nullable=False)
    person = db.Column(db.String(18), nullable=False)

    def __repr__(self):
        return '<inrecord %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'pid': self.pid,
            'sid': self.sid,
            'in_time': self.in_time,
            'price': self.price,
            'amount': self.amount,
            'money': self.money,
            'person': self.person
        }


class Inventory(db.Model):
    __tablename__ = 'inventory'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=False)
    sid = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<inventory %r>' % self.pid

    def to_dict(self):
        return {
            'pid': self.pid,
            'sid': self.sid,
            'amount': self.amount
        }


class Manager(db.Model):
    __tablename__ = 'manager'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(18), nullable=False)
    password = db.Column(db.String(18), nullable=False)

    def __repr__(self):
        return '<manager %r>' % self.account

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.account,
            'password': self.password
        }

    def check_password(self, password):
        return self.password == password


class Outrecord(db.Model):
    __tablename__ = 'outrecord'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    out_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    money = db.Column(db.DECIMAL(10, 2), nullable=False)
    person = db.Column(db.String(18), nullable=False)

    def __repr__(self):
        return '<outrecord %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'cid': self.cid,
            'pid': self.pid,
            'out_time': self.out_time,
            'price': self.price,
            'amount': self.amount,
            'money': self.money,
            'person': self.person
        }


class Product(db.Model):
    __tablename__ = 'product'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    sid = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<product %r>' % self.name

    def to_dict(self):
        return {
            'pid': self.pid,
            'name': self.name,
            'type': self.type,
            'unit': self.unit,
            'sid': self.sid,
            'category': self.category
        }


class Supplier(db.Model):
    __tablename__ = 'supplier'
    sid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    remark = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<supplier %r>' % self.name

    def to_dict(self):
        return {
            'sid': self.sid,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'remark': self.remark
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    sid = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    money = db.Column(db.DECIMAL(10, 2), nullable=False)
    book_time = db.Column(db.DateTime, nullable=False)
    order_time = db.Column(db.DateTime, nullable=False)
    remark = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<order %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'cid': self.cid,
            'pid': self.pid,
            'sid': self.sid,
            'price': self.price,
            'amount': self.amount,
            'money': self.money,
            'book_time': self.book_time,
            'order_time': self.order_time,
            'remark': self.remark
        }


class Order_detail(db.Model):
    __tablename__ = 'order_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    sid = db.Column(db.Integer, nullable=False)
    book_time = db.Column(db.DateTime, nullable=False)
    order_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    money = db.Column(db.DECIMAL(10, 2), nullable=False)
    method = db.Column(db.String(8), nullable=False)
    pay_time = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    person = db.Column(db.String(18), nullable=False)
    state = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return '<order_detail %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'cid': self.cid,
            'pid': self.pid,
            'sid': self.sid,
            'book_time': self.book_time,
            'order_time': self.order_time,
            'price': self.price,
            'amount': self.amount,
            'money': self.money,
            'method': self.method,
            'pay_time': self.pay_time,
            'address': self.address,
            'person': self.person,
            'state': self.state
        }

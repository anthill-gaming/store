# For more details, see
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#declare-a-mapping
from anthill.framework.db import db
from anthill.framework.utils import timezone
from anthill.framework.utils.translation import translate_lazy as _
from sqlalchemy_utils.types import JSONType, ChoiceType


class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=True, unique=True)
    payload = db.Column(JSONType, nullable=False, default={})
    orders = db.relationship('Order', backref='store', lazy='dynamic')
    items = db.relationship('Item', backref='store', lazy='dynamic')
    active = db.Column(db.Boolean, nullable=False, default=True)


class Item(db.Model):
    __tablename__ = 'items'
    __table_args__ = (
        db.UniqueConstraint('store_id', 'name'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    name = db.Column(db.String(128), nullable=True)
    orders = db.relationship('Order', backref='item', lazy='dynamic')
    active = db.Column(db.Boolean, nullable=False, default=True)


class Order(db.Model):
    __tablename__ = 'orders'

    STATUSES = (
        ('new', _('New')),
        ('created', _('Created')),
        ('failed', _('Failed')),
        ('retry', _('Retry')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('succeeded', _('Succeeded')),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(ChoiceType(STATUSES), default='new')
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    user_id = db.Column(db.Integer, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'))
    payload = db.Column(JSONType, nullable=False, default={})
    count = db.Column(db.Integer, default=1)
    created = db.Column(db.DateTime, default=timezone.now)
    updated = db.Column(db.DateTime, onupdate=timezone.now)


class Currency(db.Model):
    __tablename__ = 'currencies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=True, unique=True)

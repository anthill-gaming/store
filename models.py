# For more details, see
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#declare-a-mapping
from anthill.framework.db import db
from anthill.framework.utils import timezone
from anthill.framework.utils.translation import translate_lazy as _
from anthill.platform.api.internal import InternalAPIMixin
from anthill.platform.auth import RemoteUser
from sqlalchemy_utils.types import JSONType, ChoiceType
from store.payment import _get_backends


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
    name = db.Column(db.String(128), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    payload = db.Column(JSONType, nullable=False, default={})
    orders = db.relationship('Order', backref='item', lazy='dynamic')
    active = db.Column(db.Boolean, nullable=False, default=True)

    def description(self, lang):
        raise NotImplementedError

    def title(self, lang):
        raise NotImplementedError


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=True, unique=True)
    scheme = db.Column(JSONType, nullable=False, default={})
    items = db.relationship('Item', backref='category', lazy='dynamic')
    active = db.Column(db.Boolean, nullable=False, default=True)


class Order(InternalAPIMixin, db.Model):
    __tablename__ = 'orders'

    STATUSES = [
        ('new', _('New')),
        ('created', _('Created')),
        ('failed', _('Failed')),
        ('retry', _('Retry')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('succeeded', _('Succeeded')),
    ]
    PAYMENT_BACKENDS = [
        (path, path) for _, path in _get_backends(return_tuples=True)
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(ChoiceType(STATUSES), default='new')
    payment_backend = db.Column(ChoiceType(PAYMENT_BACKENDS))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'))
    user_id = db.Column(db.Integer, nullable=False)
    payload = db.Column(JSONType, nullable=False, default={})
    count = db.Column(db.Integer, default=1)
    created = db.Column(db.DateTime, default=timezone.now)
    updated = db.Column(db.DateTime, onupdate=timezone.now)

    async def get_user(self) -> RemoteUser:
        data = await self.internal_request('login', 'get_user', user_id=self.user_id)
        return RemoteUser(**data)

    def price(self, currency: str) -> float:
        raise NotImplementedError

    def price_total(self, currency: str) -> float:
        return self.price(currency) * self.count


class Currency(db.Model):
    __tablename__ = 'currencies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=True, unique=True)
    title = db.Column(db.String(128), nullable=True, unique=True)
    symbol = db.Column(db.String(128), nullable=True, unique=True)
    format = db.Column(db.String(128), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

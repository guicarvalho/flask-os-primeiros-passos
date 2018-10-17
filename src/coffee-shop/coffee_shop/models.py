from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


db = SQLAlchemy()
migrate = Migrate()


class Sale(db.Model):

    __tablename__ = 'sale'

    uuid = db.Column(UUID, primary_key=True)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    user_uuid = db.Column(UUID, db.ForeignKey('user.uuid'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Sale (uuid: {self.uuid}, value: {self.value}, user_uuid: {self.user_uuid})'


class ProductSale(db.Model):

    __tablename__ = 'product_sale'

    uuid = db.Column(UUID, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
    product_uuid = db.Column(UUID, db.ForeignKey('product.uuid'), nullable=False)
    sale_uuid = db.Column(UUID, db.ForeignKey('sale.uuid'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'uuid: {self.uuid}, quantity: {self.quantity}, value: {self.value}, product_uuid: {self.product_uuid},' \
                'sale_uuid: {sale.uuid}'


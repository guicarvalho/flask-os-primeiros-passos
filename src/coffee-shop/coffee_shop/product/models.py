from sqlalchemy.dialects.postgresql import UUID

from .. import db
from ..commons import CRUDMixin


class Product(CRUDMixin, db.Model):

    __tablename__ = 'product'

    uuid = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'Product (uuid: {self.uuid}, name: {self.name}, stock: {self.stock}, value: {self.value})'

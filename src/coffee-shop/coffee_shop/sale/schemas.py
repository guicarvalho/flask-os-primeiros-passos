from marshmallow import validate as mv

from .. import ma
from .models import Sale


class ProductSaleSchema(ma.Schema):
    product_uuid = ma.UUID(required=True)
    quantity = ma.Int(required=True, validate=mv.Range(min=1))

    class Meta:
        strict = True


class SaleCreateSchema(ma.Schema):
    products = ma.List(ma.Nested(ProductSaleSchema), required=True)

    class Meta:
        strict = True


class SaleSchema(ma.ModelSchema):
    value = ma.Number()

    class Meta:
        model=Sale

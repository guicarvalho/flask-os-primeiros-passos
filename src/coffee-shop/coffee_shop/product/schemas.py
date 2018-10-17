from marshmallow import validate as mv

from .. import ma
from .models import Product


class ProductSchema(ma.ModelSchema):
    value = ma.Number()

    class Meta:
        model = Product


class ProductCreateSchema(ma.ModelSchema):
    value = ma.Number(required=True, validate=mv.Range(min=0, max=99999999.99))
    stock = ma.Int(required=True, validate=mv.Range(min=0, max=9999))

    class Meta:
        strict = True
        model = Product
        fields = ('name', 'value', 'stock',)


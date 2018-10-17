from http import HTTPStatus

from flask import request, Blueprint
from flask_restful import Resource, Api

from .models import Product
from .schemas import ProductCreateSchema, ProductSchema


product_bp = Blueprint('product', __name__)
api = Api(product_bp)


class ProductResource(Resource):

    def get(self, uuid):
        product = Product.query.filter_by(uuid=uuid).one()
        return ProductSchema().dump(product).data

    def patch(self, uuid):
        # FIXME: adicionar mecanismo para validar os campos.
        product_data = request.json
        product = Product.query.filter_by(uuid=uuid).one()
        product.name = product_data['name']
        product.save()
        return {'name': product.name, 'value': str(product.value)}

    def delete(self, uuid):
        product = Product.query.filter_by(uuid=uuid).one()
        product.delete()
        return {}


class ProductsResource(Resource):

    def get(self):
        products = Product.query.all()
        return ProductSchema(many=True).dump(products).data

    def post(self):
        product = ProductCreateSchema().load(request.json).data
        product.save()
        return ProductSchema().dump(product).data, HTTPStatus.CREATED


api.add_resource(ProductResource, '/api/v1/products/<uuid>')
api.add_resource(ProductsResource, '/api/v1/products')

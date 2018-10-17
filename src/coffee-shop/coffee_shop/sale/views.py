from http import HTTPStatus

from flask import Blueprint, request
from flask_restful import Api

from ..auth.models import User
from ..auth.services import get_identity
from ..core.resources import AuthenticatedResource
from .models import ProductSale, Sale
from .schemas import SaleSchema


sale_bp = Blueprint('sale', __name__)
api = Api(sale_bp)

# class ProductResource(Resource):

#     def get(self, uuid):
#         product = Product.query.filter_by(uuid=uuid).one()
#         return ProductSchema().dump(product).data

#     def patch(self, uuid):
#         # FIXME: adicionar mecanismo para validar os campos.
#         product_data = request.json
#         product = Product.query.filter_by(uuid=uuid).one()
#         product.name = product_data['name']
#         product.save()
#         return {'name': product.name, 'value': str(product.value)}

#     def delete(self, uuid):
#         product = Product.query.filter_by(uuid=uuid).one()
#         product.delete()
#         return {}

class SalesResource(AuthenticatedResource):

    def get(self):
        sales = Sale.query.all()
        return SaleSchema(many=True).dump(sales).data

    def post(self):
        sale_data = SaleCreateSchema().load(request.json).data

        user_identity = get_identity()
        user = User.query.filter_by(email=user_identity).one()

        sale = Sale(value=0, user_uuid=user.uuid)
        sale.save()
        return {'uuid': sale.uuid}, HTTPStatus.CREATED


#api.add_resource(ProductResource, '/api/v1/products/<uuid>')
api.add_resource(SalesResource, '/api/v1/sales')

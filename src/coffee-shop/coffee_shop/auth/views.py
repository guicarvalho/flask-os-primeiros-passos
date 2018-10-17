from http import HTTPStatus

from flask import request, Blueprint
from flask_restful import Resource, Api

from ..core.resources import AuthenticatedResource
from .models import Role, User
from .schemas import LoginSchema, RoleCreateSchema, RoleSchema, UserCreateSchema, UserSchema
from .services import create_token, requires_roles


auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)


class LoginResource(Resource):

    def post(self):
        data = LoginSchema().load(request.json).data

        user = User.query.filter_by(email=data['username']).one()

        if user.password == data['password']:  # FIXME: criptografar senha
            access_token = create_token(data['username'])
            return {'access_token': access_token}, HTTPStatus.OK


class UsersResource(AuthenticatedResource):

    def get(self):
        users = User.query.all()
        return UserSchema(many=True).dump(users)

    @requires_roles('editor')
    def post(self):
        user = UserCreateSchema().load(request.json).data
        user.save()
        return UserSchema().dump(user).data, HTTPStatus.CREATED


class UserResource(AuthenticatedResource):

    def get(self, uuid):
        user = User.query.filter_by(uuid=uuid).one()
        return UserSchema().dump(user).data

    def patch(self, uuid):
        data = request.json

        user = User.query.filter_by(uuid=uuid).one()

        for field in data:
            if field == 'email':
                raise InvalidUsage('email nao pode alterar', HTTPStatus.CONFLICT)
            setattr(user, field, data[field])
        user.save()

        return UserSchema().dump(user).data, HTTPStatus.OK

    def delete(self, uuid):
        user = User.query.filter_by(uuid=uuid).one()
        user.delete()
        return {}


class RolesResource(AuthenticatedResource):

    def get(self):
        roles = Role.query.all()
        return RoleSchema(many=True).dump(roles).data

    def post(self):
        role = RoleCreateSchema().load(request.json).data
        role.save()
        return RoleSchema().dump(role).data, HTTPStatus.CREATED


class RoleResource(AuthenticatedResource):

    def get(self, uuid):
        role = Role.query.filter_by(uuid=uuid).one()
        return RoleSchema().dump(role).data


api.add_resource(LoginResource, '/api/v1/login')
api.add_resource(UsersResource, '/api/v1/users')
api.add_resource(UserResource, '/api/v1/users/<uuid>', endpoint='user')
api.add_resource(RolesResource, '/api/v1/roles')
api.add_resource(RoleResource, '/api/v1/roles/<uuid>', endpoint='role')


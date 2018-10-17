from marshmallow import post_load, validate as mv

from .. import ma
from .models import Role, User


class LoginSchema(ma.Schema):
    username = ma.Str(required=True)
    password = ma.Str(required=True)

    class Meta:
        strict = True


class UserSchema(ma.ModelSchema):
    role = ma.HyperlinkRelated(endpoint='auth.role', url_key='uuid')

    class Meta:
        model = User


class UserCreateSchema(ma.Schema):
    name = ma.Str(required=True, validate=mv.Length(max=50))
    email = ma.Email(required=True, validate=mv.Length(max=80))
    password = ma.Str(required=True, validate=mv.Length(max=20))
    active = ma.Bool(required=False, missing=True)
    role = ma.Str(required=True)

    class Meta:
        strict = True
        fields = ('name', 'email', 'password', 'active', 'role',)

    @post_load
    def _make_user(self, data):
        data['role'] = Role.query.filter_by(name=data['role']).one()
        return User(**data)


class RoleSchema(ma.ModelSchema):
    users = ma.List(ma.HyperlinkRelated(endpoint='auth.user', url_key='uuid'))

    class Meta:
        model = Role


class RoleCreateSchema(ma.ModelSchema):
    name = ma.Str(required=True, validate=mv.Length(max=20))

    class Meta:
        strict = True
        model = Role
        fields = ('name',)

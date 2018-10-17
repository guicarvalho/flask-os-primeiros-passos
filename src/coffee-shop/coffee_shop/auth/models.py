from sqlalchemy.dialects.postgresql import UUID

from .. import db
from ..commons import CRUDMixin


class User(CRUDMixin, db.Model):

    __tablename__ = 'user'

    uuid = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    role_uuid = db.Column(db.ForeignKey('role.uuid'))
    role = db.relationship('Role', backref='users')

    def __repr__(self):
        return f'User (uuid: {self.uuid}, name: {self.name}, email: {self.email}, active: {self.active}, role: {self.role})'


class Role(CRUDMixin, db.Model):

    __tablename__ = 'role'

    uuid = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'Role (uuid: {self.uuid}), name: {self.name}'

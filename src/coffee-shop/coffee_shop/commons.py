from datetime import datetime
from uuid import uuid4

from . import db


class CreatedMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        if not self.uuid:
            self.uuid = uuid4().hex
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class CRUDMixin(CreatedMixin):
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

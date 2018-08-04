import uuid
from datetime import datetime

from tastore import db
from .constants import TASKAPP_STATUS


def get_uuid():
    return str(uuid.uuid4())


class TaskApp(db.Model):
    app_id = db.Column(db.String(40), primary_key=True, default=get_uuid)
    name = db.Column(db.String(40), nullable=False)
    author_id = db.Column(db.String(40), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    last_update = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    downloads = db.Column(db.Integer(), nullable=False, default=0)
    price = db.Column(db.Float(), nullable=False, default=0)
    current_task = db.Column(db.String(40))
    description = db.Column(db.String(2000))
    status = db.Column(db.String(20), nullable=False, default=TASKAPP_STATUS.ACTIVE)

    _meta = ['name', 'description']

    def update(self, data):
        for key in self._meta:
            if key in data:
                setattr(self, key, data[key])
        db.session.add(self)

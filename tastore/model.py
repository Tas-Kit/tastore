import uuid
from datetime import datetime
from werkzeug.exceptions import BadRequest

from tastore import db
from .constants import TASKAPP_STATUS
from util import taskservice


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

    def assert_current_task(self):
        if self.current_task is None:
            error = BadRequest('Unable to find a binding task from this Task App')
            error.status_code = 404
            raise error

    def update(self, data):
        for key in self._meta:
            if key in data:
                setattr(self, key, data[key])
        db.session.add(self)

    def preview(self):
        self.assert_current_task()
        return taskservice.preview_task(self.current_task)

    def download(self, uid):
        self.assert_current_task()
        task = taskservice.download_task(self.current_task, uid)
        self.downloads += 1
        db.session.add(self)
        return task

    def upload(self, tid, uid):
        task = taskservice.upload_task(tid, uid, self.current_task)
        if self.current_task is None:
            self.current_task = task['tid']
            db.session.add(self)
        return task

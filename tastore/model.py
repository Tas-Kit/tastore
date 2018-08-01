from tastore import db
import uuid


def get_uuid():
    return str(uuid.uuid4())


class TaskApp(db.Model):
    app_id = db.Column(db.String(36), primary_key=True, default=get_uuid)

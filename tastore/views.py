# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from flask import Blueprint
from flask_restplus import Api, Resource, fields, reqparse
from datetime import datetime

from .model import TaskApp
from tastore import db
from .constants import TASKAPP_STATUS
from .config import PER_PAGE

main_blueprint = Blueprint('main', __name__, template_folder='templates')


api = Api(main_blueprint, version='1.0', title='Task App API',
          description='Task App API')

task_app_model = api.model('Task App', {
    'app_id': fields.String(readOnly=True,
                            description='The task unique identifier'),
    'name': fields.String(required=True,
                          description='The task name'),
    'author_id': fields.String(readOnly=True,
                               description='The user id of the author'),
    'created_date': fields.DateTime(readOnly=True,
                                    dt_format='rfc822',
                                    description='The date time when this task app is created'),
    'last_update': fields.DateTime(readOnly=True,
                                   dt_format='rfc822',
                                   description='The last time when this task app is updated'),
    'downloads': fields.Integer(readonly=True,
                                description='Number of downloads'),
    'status': fields.String(choices=(
        TASKAPP_STATUS.ACTIVE,
        TASKAPP_STATUS.INACTIVE,
        TASKAPP_STATUS.SUSPENDED),
        description='The status of the Task App. ACTIVE, INACTIVE, SUSPENDED'),
    'price': fields.Float(description='The price of each task app download'),
    'description': fields.String(description='The description of the task app'),
    'current_task': fields.String(description='The tid of the task in the task app')
})


ns = api.namespace('TaskApp', description='Task App operations')


def register_blueprints(app):
    app.register_blueprint(main_blueprint, url_prefix='/api/v1/tastore')

# Basic parser for parsing uid in cookie section
parser = reqparse.RequestParser()
parser.add_argument('uid', type=str, location='cookies')

task_app_parser = reqparse.RequestParser()
task_app_parser.add_argument('name', required=True, type=str, location='form')
task_app_parser.add_argument('description', type=str, location='form')

task_app_list_parser = reqparse.RequestParser()
task_app_list_parser.add_argument('keyword', type=str, location='args')
task_app_list_parser.add_argument('author_id', type=str, location='args')

tid_parser = reqparse.RequestParser()
tid_parser.add_argument('tid', type=str, location='form', required=True)


@ns.route('/')
class TaskAppListView(Resource):

    @ns.doc('keyword Task App', params={
        'keyword': 'String for keyword',
        'author_id': "Author's uid"
    })
    @api.marshal_list_with(task_app_model, envelope='task_app_list')
    def get(self):
        """
        Only show active task, unless the user is querying his own tasks.
        """
        args = task_app_list_parser.parse_args()
        keyword = args['keyword']
        uid = parser.parse_args()['uid']
        author_id = args['author_id']
        query = TaskApp.query

        # Check if author is querying his own tasks
        if uid != author_id:
            query = query.filter_by(status=TASKAPP_STATUS.ACTIVE)

        # Filter task by author id
        if author_id is not None:
            query = query.filter_by(author_id=author_id)

        # Search keywords
        if keyword is not None and keyword != '':
            ilike_query = TaskApp.name.ilike('%{0}%'.format(keyword))
            query = query.filter(ilike_query)

        return query.paginate(per_page=PER_PAGE).items

    @ns.doc('Create Task App', parser=task_app_parser)
    @api.marshal_with(task_app_model, envelope='task_app')
    def post(self):
        """
        Create a task app
        """
        args = parser.parse_args()
        uid = args['uid']
        task_app = TaskApp()
        task_app.author_id = uid
        task_app.update(task_app_parser.parse_args())
        db.session.commit()
        return task_app


@ns.route('/<string:app_id>/')
class TaskAppView(Resource):

    @ns.doc('get_task_app')
    @api.marshal_with(task_app_model)
    def get(self, app_id):
        """
        Get the task app by app_id
        """
        return TaskApp.query.filter_by(app_id=app_id).first()

    @ns.doc('partially_update_task_app', parser=task_app_parser)
    @api.marshal_with(task_app_model)
    def patch(self, app_id):
        """
        Partially update the task app
        """
        task_app = TaskApp.query.filter_by(app_id=app_id).first()
        task_app.last_update = datetime.utcnow()
        task_app.update(task_app_parser.parse_args())
        db.session.commit()
        return task_app


# @ns.route('/<string:app_id>/upload_task/')
# class UploadTaskApp(Resource):

#     @ns.doc('upload_task')
#     @ns.expect(tid_parser, validate=True)
#     @ns.marshal_with()
#     def post(self, app_id):
#         pass

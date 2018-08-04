# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from flask import Blueprint
from flask_restplus import Api, Resource, fields, reqparse
from .model import TaskApp
from tastore import db
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
    'create_date': fields.DateTime(readOnly=True,
                                   dt_format='rfc822',
                                   description='The date time when this task app is created'),
    'last_update': fields.DateTime(readOnly=True,
                                   dt_format='rfc822',
                                   description='The last time when this task app is updated'),
    'downloads': fields.Integer(readonly=True,
                                description='Number of downloads'),
    'status': fields.String(description='The status of the Task App. ACTIVE, INACTIVE, SUSPENDED'),
    'price': fields.Float(description='The price of each task app download'),
    'description': fields.String(required=True, description='The description of the task app'),
    'current_task': fields.String(description='The tid of the task in the task app')
})


ns = api.namespace('TaskApp', description='Task App operations')


def register_blueprints(app):
    app.register_blueprint(main_blueprint, url_prefix='/api/v1/tastore')

parser = reqparse.RequestParser()
parser.add_argument('search', type=str, location='args')
parser.add_argument('uid', type=str, location='cookies')


@ns.route('/')
class TaskAppListView(Resource):

    @ns.doc('Search Task App', params={'search': 'String for search'})
    @ns.marshal_list_with(task_app_model)
    def get(self):
        args = parser.parse_args()
        search = args['search']
        if search is None or search == '':
            return TaskApp.query.limit(PER_PAGE).all()
        else:
            query = TaskApp.name.ilike('%{0}%'.format(search))
            return TaskApp.query.filter(query).paginate(per_page=PER_PAGE).items

    @ns.doc('Create Task App')
    @ns.expect(task_app_model, validate=True)
    @api.marshal_with(task_app_model)
    def post(self):
        args = parser.parse_args()
        uid = args['uid']
        task_app = TaskApp()
        task_app.author_id = uid
        task_app.update(api.payload)
        db.session.commit()
        return task_app

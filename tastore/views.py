# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from flask import Blueprint
from flask_restplus import Api, Resource, fields

main_blueprint = Blueprint('main', __name__, template_folder='templates')


api = Api(main_blueprint, version='1.0', title='TodoMVC API',
          description='A simple TodoMVC API')

task_app = api.model('Task App', {
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
    'status': fields.String(description='The status of the Task App. ACTIVE, INACTIVE, SUSPENDED')
})


def register_blueprints(app):
    app.register_blueprint(main_blueprint, url_prefix='/api/v1/tastore')

ns = api.namespace('TaskApp', description='Task App operations')


@ns.route('/')
class TaskAppListView(Resource):

    @ns.doc('Search Task App', params={'id': 'An ID'})
    def get(self, name):
        return 'SUCCESS'

    @ns.doc('Create Task App')
    @ns.expect(task_app)
    @api.marshal_with(task_app)
    def post(self):
        return api.payload

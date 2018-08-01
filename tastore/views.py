# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from flask import Blueprint
from flask_restplus import Api, Resource

main_blueprint = Blueprint('main', __name__, template_folder='templates')


api = Api(main_blueprint, version='1.0', title='TodoMVC API',
          description='A simple TodoMVC API')


def register_blueprints(app):
    app.register_blueprint(main_blueprint, url_prefix='/api/v1/tastore')

ns = api.namespace('todos', description='TODO operations')


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos', params={'id': 'An ID'})
    def get(self):
        '''List all tasks'''
        return 'SUCCESS'

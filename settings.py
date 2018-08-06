import os

ENV = os.getenv('ENV', 'DEV')

DEBUG = ENV == 'PROD'
PER_PAGE = os.getenv('PER_PAGE', 30)
TASKSERVICE_HOST = os.getenv('TASKSERVICE_HOST', 'taskservice')
TASKSERVICE_PORT = os.getenv('TASKSERVICE_HOST', '8000')
TASKSERVICE_VERSION = os.getenv('TASKSERVICE_VERSION', 'v1')


# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.sqlite'

if ENV != 'DEV':
    DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypassword')
    DB_HOST = os.getenv('DB_HOST', 'tastoredb')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_DATABASE = os.getenv('DB_DATABASE', 'postgres')
    # 'postgresql+psycopg2://username:mypass@localhost:5432/test-db'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'.format(
        username=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE
    )

import requests
from ..config import TASKSERVICE_HOST, TASKSERVICE_PORT, TASKSERVICE_VERSION

base_url = 'http://{0}:{1}/api/{2}/taskservice/'.format(TASKSERVICE_HOST, TASKSERVICE_PORT, TASKSERVICE_VERSION)

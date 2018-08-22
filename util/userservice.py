import requests
from flask import abort

from settings import USERSERVICE_HOST, USERSERVICE_PORT, USERSERVICE_VERSION

base_url = 'http://{0}:{1}/api/{2}/userservice/'.format(USERSERVICE_HOST, USERSERVICE_PORT, USERSERVICE_VERSION)


def handler(func):
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        data = resp.json()
        if 'status_code' in data and data['status_code'] >= 400:
            abort(data['status_code'], data['detail'])
        return data['results']
    return wrapper


@handler
def get_users_info(uid_list):
    query = '&'.join(['uid=' + uid for uid in uid_list])
    return requests.get('{0}users/?{query}'.format(base_url, query=query))

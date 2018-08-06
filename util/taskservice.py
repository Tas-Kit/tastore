import requests
from flask import abort

from settings import TASKSERVICE_HOST, TASKSERVICE_PORT, TASKSERVICE_VERSION

base_url = 'http://{0}:{1}/api/{2}/taskservice/'.format(TASKSERVICE_HOST, TASKSERVICE_PORT, TASKSERVICE_VERSION)


def handler(func):
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        data = resp.json()
        if 'status_code' in data and data['status_code'] >= 400:
            abort(data['status_code'], data['detail'])
        return data
    return wrapper


@handler
def delete_task(tid):
    return requests.delete('{0}internal/task/{tid}/'.format(base_url, tid=tid))


@handler
def upload_task(tid, uid, target_tid=None):
    return requests.post(
        '{0}internal/task/{tid}/'.format(base_url, tid=tid),
        data={
            'uid': uid,
            'target_tid': target_tid
        })


@handler
def preview_task(tid):
    return requests.get('{0}internal/task/{tid}/'.format(base_url, tid=tid))


@handler
def download_task(tid, uid):
    return requests.post('{0}internal/task/{tid}/download/'.format(base_url, tid=tid),
                         data={'uid': uid})

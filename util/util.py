from .userservice import get_users_info


def collect_user_info(task_apps):
    uid_set = set()
    for task_app in task_apps:
        uid_set.add(task_app.author_id)
    users = get_users_info(uid_set)
    print(users)
    user_map = {user['uid']: user for user in users}
    for task_app in task_apps:
        if task_app.author_id in user_map:
            task_app.author = user_map[task_app.author_id]
    return task_apps

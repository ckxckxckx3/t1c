from functools import wraps

from flask import abort, session

from db import query_one
from permissions import ROLE_PERMISSIONS


def current_user():
    uid = session.get("uid")
    if uid is None:
        return None
    return query_one("SELECT id, email, role FROM users WHERE id = ?", (uid,))


def require_permission(permission):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user()
            if user is None:
                abort(401)
            if permission not in ROLE_PERMISSIONS.get(user["role"], set()):
                abort(403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator

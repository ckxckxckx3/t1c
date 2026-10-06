from flask import Blueprint, abort, jsonify, request

from auth import require_permission
from permissions import ROLE_PERMISSIONS
from db import execute, query_all

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get("")
@require_permission("users:read")
def list_users():
    rows = query_all("SELECT id, email, role FROM users")
    return jsonify([dict(r) for r in rows])


@bp.patch("/<int:user_id>/role")
@require_permission("users:manage")
def set_user_role(user_id):
    role = request.get_json(force=True)["role"]
    if role not in ROLE_PERMISSIONS:
        abort(400)
    execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
    return jsonify({"status": "updated"})

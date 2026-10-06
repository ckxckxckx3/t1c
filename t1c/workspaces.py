from flask import Blueprint, jsonify

from auth import require_permission
from db import get_db, query_all

bp = Blueprint("workspaces", __name__, url_prefix="/workspaces")


@bp.get("")
@require_permission("workspace:read")
def list_workspaces():
    rows = query_all("SELECT id, name FROM workspaces")
    return jsonify([dict(r) for r in rows])


@bp.delete("/<int:workspace_id>")
@require_permission("workspace:delete")
def delete_workspace(workspace_id):
    db = get_db()
    db.execute("DELETE FROM documents WHERE workspace_id = ?", (workspace_id,))
    db.execute("DELETE FROM workspaces WHERE id = ?", (workspace_id,))
    db.commit()
    return jsonify({"status": "deleted"})

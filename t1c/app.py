import os

from flask import Flask, abort, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from db import close_db, execute, query_one
from users import bp as users_bp
from workspaces import bp as workspaces_bp

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.teardown_appcontext(close_db)
app.register_blueprint(workspaces_bp)
app.register_blueprint(users_bp)


@app.post("/register")
def register():
    data = request.get_json(force=True)
    execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        (data["email"], generate_password_hash(data["password"])),
    )
    return jsonify({"status": "created"}), 201


@app.post("/login")
def login():
    data = request.get_json(force=True)
    user = query_one("SELECT id, password_hash FROM users WHERE email = ?", (data["email"],))
    if user is None or not check_password_hash(user["password_hash"], data["password"]):
        abort(401)
    session.clear()
    session["uid"] = user["id"]
    return jsonify({"status": "ok"})

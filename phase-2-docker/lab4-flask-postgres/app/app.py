import os
import json
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# App metadata (used for /version endpoint)
APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
GIT_COMMIT = os.getenv("GIT_COMMIT", "unknown")

# Database config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "devdb")
DB_USER = os.getenv("DB_USER", "devuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devpass123")

def get_db_connection():
    conn = psycopg2.connect(
	host=DB_HOST,
	port=DB_PORT,
	dbname=DB_NAME,
	user=DB_USER,
	password=DB_PASSWORD,
	cursor_factory=RealDictCursor,
    )
    return conn

def init_db():
    """Create users table if it does not exist."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
	"""
	CREATE TABLE IF NOT EXISTS users(
	    id SERIAL PRIMARY KEY,
	    name TEXT NOT NULL,
	    email TEXT NOT NULL UNIQUE
	);
	"""
    )
    conn.commit()
    cur.close()
    conn.close()

@app.route("/health", methods=["GET"])
def health():
    """Basic health check + DB connectivity check."""
    try:
	conn= = get_db_connection()
	cur = conn.cursor()
	cur.execute("SELECT 1 AS ok;")
	cur.fetchone()
	cur.close()
	conn.close()
	db_status = "up"
    except Exception as e:
	db_status = f"down: {e}"

    return jsonify(
	{
	    "status": "ok",
	    "db": db_status,
	}
    )

@app.route("/users", methods=["GET"])
def list_users():
    """Return all users."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users ORDER BY id;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

@app.route("/users", metrhods=["POST"]
def create_user():
    """Create a new user from JSON body: {name, email}."""
    data = request.get.json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
	return jsonify({"error": "name and email are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
	cur.execute(
	     "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email;",
	     (name, email),
	)
	user = cur.fethone()
	conn.commit()
    except Exception as e:
	conn.rollback()
	return jsonify({"error": str(e)}), 400
    finally:
	cur.close()
	conn.close()

    return jsonify(user), 201

if __name__ == "__main__":
    # Only for local dev (not used in Docker)
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("BACKEND_PORT", "5000")))

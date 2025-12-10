import os
import time

from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import psutil

app = Flask(__name__)

# App metadata for /version
APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
GIT_COMMIT = os.getenv("GIT_COMMIT", "unknown")

# DB Config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "devdb")
DB_USER = os.getenv("DB_USER", "devuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devpass123")

# Uptime start
START_TIME = time.time()


def get_db_connection():
    """Open DB connection."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor,
    )
    return conn


def ensure_users_table():
    """Create table if missing."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
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
    """Check app + DB."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        db_state = "up"
    except Exception as e:
        db_state = f"down: {e}"

    return jsonify({"service": "users-api", "status": "ok", "db": db_state})


@app.route("/version", methods=["GET"])
def version():
    return jsonify(
        {"service": "users-api", "app_version": APP_VERSION, "git_commit": GIT_COMMIT}
    )


@app.route("/users", methods=["GET"])
def list_users():
    ensure_users_table()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/users", methods=["POST"])
def create_user():
    """Create user from JSON body."""
    ensure_users_table()
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO users (name, email)
            VALUES (%s, %s)
            RETURNING id, name, email;
            """,
            (name, email),
        )
        new_user = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify(new_user), 201


def get_system_metrics():
    uptime = time.time() - START_TIME
    cpu_percent = psutil.cpu_percent(interval=0.2)
    mem = psutil.virtual_memory()
    return uptime, cpu_percent, mem.percent


def get_users_count():
    ensure_users_table()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS count FROM users;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result["count"]


@app.route("/metrics", methods=["GET"])
def metrics():
    """Prometheus-style metrics endpoint."""
    uptime, cpu, mem = get_system_metrics()
    users_count = get_users_count()

    response = (
        "# HELP app_uptime_seconds Application uptime in seconds\n"
        "# TYPE app_uptime_seconds gauge\n"
        f"app_uptime_seconds {uptime}\n\n"
        "# HELP app_cpu_percent CPU usage percent\n"
        "# TYPE app_cpu_percent gauge\n"
        f"app_cpu_percent {cpu}\n\n"
        "# HELP app_memory_percent Memory usage percent\n"
        "# TYPE app_memory_percent gauge\n"
        f"app_memory_percent {mem}\n\n"
        "# HELP users_total Number of users\n"
        "# TYPE users_total gauge\n"
        f"users_total {users_count}\n"
    )

    return response, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/load", methods=["GET"])
def load():
    """Generate CPU load for N seconds for testing."""
    seconds = int(request.args.get("seconds", 5))
    end_time = time.time() + seconds

    while time.time() < end_time:
        _ = sum(i * i for i in range(5000))

    return jsonify({"status": "ok", "load_generated_seconds": seconds})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("BACKEND_PORT", "5000")))

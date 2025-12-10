import os
import time

from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import psutil

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
GIT_COMMIT = os.getenv("GIT_COMMIT", "unknown")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "devdb")
DB_USER = os.getenv("DB_USER", "devuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devpass123")

START_TIME = time.time()


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


def ensure_tasks_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'open',
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
        );
    """
    )
    conn.commit()
    cur.close()
    conn.close()


@app.route("/health", methods=["GET"])
def health():
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

    return jsonify({"service": "tasks-api", "status": "ok", "db": db_state})


@app.route("/version", methods=["GET"])
def version():
    return jsonify(
        {"service": "tasks-api", "app_version": APP_VERSION, "git_commit": GIT_COMMIT}
    )


@app.route("/tasks", methods=["GET"])
def list_tasks():
    ensure_tasks_table()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, title, description, status, user_id
        FROM tasks
        ORDER BY id;
    """
    )
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    ensure_tasks_table()
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    description = data.get("description")
    user_id = data.get("user_id")

    if not title:
        return jsonify({"error": "title is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO tasks (title, description, user_id)
            VALUES (%s, %s, %s)
            RETURNING id, title, description, status, user_id;
            """,
            (title, description, user_id),
        )
        task = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    ensure_tasks_table()
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    title = data.get("title")
    description = data.get("description")

    if not any([status, title, description]):
        return jsonify({"error": "nothing to update"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE tasks
            SET
                title = COALESCE(%s, title),
                description = COALESCE(%s, description),
                status = COALESCE(%s, status)
            WHERE id = %s
            RETURNING id, title, description, status, user_id;
            """,
            (title, description, status, task_id),
        )
        updated = cur.fetchone()
        if updated is None:
            conn.rollback()
            return jsonify({"error": "task not found"}), 404
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify(updated), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    ensure_tasks_table()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM tasks WHERE id = %s RETURNING id;",
            (task_id,),
        )
        deleted = cur.fetchone()
        if deleted is None:
            conn.rollback()
            return jsonify({"error": "task not found"}), 404
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

    return jsonify({"status": "deleted", "id": task_id}), 200


def get_system_metrics():
    uptime = time.time() - START_TIME
    cpu_percent = psutil.cpu_percent(interval=0.2)
    mem = psutil.virtual_memory()
    return uptime, cpu_percent, mem.percent


def get_tasks_count():
    ensure_tasks_table()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS count FROM tasks;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result["count"]


@app.route("/metrics", methods=["GET"])
def metrics():
    """Prometheus-style metrics endpoint for tasks-api."""
    uptime, cpu, mem = get_system_metrics()
    tasks_count = get_tasks_count()

    response = (
        "# HELP tasks_app_uptime_seconds Tasks service uptime in seconds\n"
        "# TYPE tasks_app_uptime_seconds gauge\n"
        f"tasks_app_uptime_seconds {uptime}\n\n"
        "# HELP tasks_app_cpu_percent CPU usage percent\n"
        "# TYPE tasks_app_cpu_percent gauge\n"
        f"tasks_app_cpu_percent {cpu}\n\n"
        "# HELP tasks_app_memory_percent Memory usage percent\n"
        "# TYPE tasks_app_memory_percent gauge\n"
        f"tasks_app_memory_percent {mem}\n\n"
        "# HELP tasks_total Number of tasks\n"
        "# TYPE tasks_total gauge\n"
        f"tasks_total {tasks_count}\n"
    )

    return response, 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/load", methods=["GET"])
def load():
    """Generate CPU load for N seconds for testing (tasks-api)."""
    seconds = int(request.args.get("seconds", 5))
    end_time = time.time() + seconds

    while time.time() < end_time:
        _ = sum(i * i for i in range(5000))

    return jsonify(
        {"service": "tasks-api", "status": "ok", "load_generated_seconds": seconds}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("BACKEND_PORT", "5000")))

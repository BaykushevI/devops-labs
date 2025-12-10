import os
import requests

TASKS_BASE_URL = os.getenv("TASKS_BASE_URL", "http://localhost:8082")

def test_health_tasks():
    """Check if /health endpoint of Tasks API works."""
    r = requests.get(f"{TASKS_BASE_URL}/health")
    assert r.status_code == 200

def test_version_tasks():
    """Check /version of Tasks API."""
    r = requests.get(f"{TASKS_BASE_URL}/version")
    assert r.status_code == 200
    # data = r.json()
    # assert "version" in data


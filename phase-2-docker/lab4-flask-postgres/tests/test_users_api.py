import os
import requests

# You can change the value depends of docker-compose.yml
USERS_BASE_URL = os.getenv("USERS_BASE_URL", "http://localhost:8081")

def test_health_users():
    """Check if endpoint /health in Users API"""
    r = requests.get(f"{USERS_BASE_URL}/health")
    assert r.status_code == 200

def test_version_users():
    """Check if return /version."""
    r = requests.get(f"{USERS_BASE_URL}/version")
    assert r.status_code == 200
    # If return JSON, remove comment to debug:
    # data = r.json()
    # assert "version" in data


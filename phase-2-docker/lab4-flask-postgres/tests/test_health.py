import requests

def test_users_api_health():
    r = requests.get("http://localhost:8081/health")
    assert r.status_code == 200

def test_tasks_api_health():
    r = requests.get("http://localhost:8082/health")
    assert r.status_code == 200


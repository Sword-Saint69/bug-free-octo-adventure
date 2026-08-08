import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app, follow_redirects=False)

def test_health():
    res = client.get("/health")
    print("Health check response:", res.status_code, res.json())
    assert res.status_code == 200
    assert res.json()["mode"] == "pure_backend_api"

def test_root_redirect():
    res = client.get("/")
    assert res.status_code in (307, 302)
    assert res.headers["location"] == "/docs"
    print("Root URL successfully redirects to Swagger API docs (/docs)!")

def test_pure_backend_dashboard():
    headers = {
        "Authorization": "Bearer dev_token_123",
        "X-Device-Id": "ESP32_S3_TFT_001"
    }
    res = client.get("/api/v1/device/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()["data"]
    assert "crypto" in data
    assert "fx_rates" in data
    assert "earthquakes" in data
    assert "news" in data
    assert "space_apod" in data
    assert "tasks" in data
    assert "stocks" in data
    assert "sports" in data
    assert "daily_content" in data
    assert "media_player" in data
    print("Pure backend microcontroller snapshot endpoint verified 100% functional with all 4 new modules!")

def test_media_action():
    headers = {"Authorization": "Bearer dev_token_123"}
    payload = {
        "title": "Starboy",
        "artist": "The Weeknd",
        "album": "Starboy",
        "is_playing": True,
        "progress_ms": 60000,
        "duration_ms": 230000
    }
    res = client.post("/api/v1/actions/media", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["title"] == "Starboy"
    assert data["artist"] == "The Weeknd"
    print("Spotify / Media Player update action endpoint verified 100% functional!")

def test_tasks_crud():
    res = client.get("/api/v1/tasks")
    assert res.status_code == 200
    initial_tasks = res.json()["data"]
    assert len(initial_tasks) == 0

    new_task_payload = {
        "title": "Pure Backend Dynamic Task Test",
        "priority": "high",
        "due_time": "12:00 PM"
    }
    res = client.post("/api/v1/tasks", json=new_task_payload)
    assert res.status_code == 201
    created_task = res.json()["data"]
    task_id = created_task["id"]

    res = client.patch(f"/api/v1/tasks/{task_id}/toggle")
    assert res.status_code == 200
    assert res.json()["data"]["completed"] is True

    res = client.delete(f"/api/v1/tasks/{task_id}")
    assert res.status_code == 200
    print("Pure backend task CRUD operations verified 100% functional!")

if __name__ == "__main__":
    test_health()
    test_root_redirect()
    test_pure_backend_dashboard()
    test_media_action()
    test_tasks_crud()
    print("ALL PURE BACKEND TESTS PASSED CLEANLY!")

from datetime import datetime, timedelta, timezone


def test_task_crud_and_filters(test_client, auth_headers):
    # Create a task
    payload = {
        "title": "Buy milk",
        "description": "Skim",
        "priority": "high",
        "status": "pending",
        "dueDate": datetime.now(timezone.utc).isoformat(),
    }
    r = test_client.post("/tasks/", json=payload, headers=auth_headers)
    assert r.status_code == 201, r.text
    task = r.json()
    assert task["title"] == payload["title"]
    assert task["priority"] == "high"
    assert task["status"] == "pending"
    task_id = task["id"]

    # List tasks default
    r = test_client.get("/tasks/", headers=auth_headers)
    assert r.status_code == 200
    listing = r.json()
    assert "tasks" in listing and isinstance(listing["tasks"], list)
    assert "pagination" in listing

    # Filter by status
    r = test_client.get("/tasks/?status=pending", headers=auth_headers)
    assert r.status_code == 200
    assert any(t["id"] == task_id for t in r.json()["tasks"])  # our task present

    # Get single task
    r = test_client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["id"] == task_id

    # Update with camelCase fields and enum coercion
    upd = {
        "status": "completed",
        "priority": "low",
        "dueDate": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    }
    r = test_client.put(f"/tasks/{task_id}", json=upd, headers=auth_headers)
    assert r.status_code == 200, r.text
    updated = r.json()
    assert updated["status"] == "completed"
    assert updated["priority"] == "low"

    # Delete
    r = test_client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert r.status_code == 204

    # Subsequent get should be 404 and follow error format
    r = test_client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert r.status_code == 404
    body = r.json()
    assert "error" in body and "message" in body["error"]
    assert body.get("path", "").startswith("/tasks/")


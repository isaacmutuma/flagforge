"""
Tests for the admin CRUD endpoints (app/routers/flags.py).
"""


def test_create_flag(client):
    response = client.post(
        "/flags",
        json={"key": "test-flag", "description": "a test", "rollout_percentage": 10},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["key"] == "test-flag"
    assert body["enabled"] is False  # default, since we didn't set it
    assert "id" in body
    assert "created_at" in body


def test_create_duplicate_flag_fails(client):
    client.post("/flags", json={"key": "dup-flag"})
    response = client.post("/flags", json={"key": "dup-flag"})
    assert response.status_code == 409


def test_get_nonexistent_flag_returns_404(client):
    response = client.get("/flags/does-not-exist")
    assert response.status_code == 404


def test_list_flags(client):
    client.post("/flags", json={"key": "flag-a"})
    client.post("/flags", json={"key": "flag-b"})
    response = client.get("/flags")
    assert response.status_code == 200
    keys = [flag["key"] for flag in response.json()]
    assert "flag-a" in keys
    assert "flag-b" in keys


def test_update_flag_persists_change(client):
    client.post("/flags", json={"key": "update-me", "rollout_percentage": 5})
    response = client.patch("/flags/update-me", json={"rollout_percentage": 50})
    assert response.status_code == 200
    assert response.json()["rollout_percentage"] == 50


def test_partial_update_does_not_wipe_other_fields(client):
    """
    This is the bug exclude_unset=True in crud.py exists to prevent —
    updating one field should never silently reset the others.
    """
    client.post(
        "/flags",
        json={"key": "partial-update", "description": "keep me", "rollout_percentage": 20},
    )
    response = client.patch("/flags/partial-update", json={"enabled": True})
    assert response.status_code == 200
    body = response.json()
    assert body["enabled"] is True
    assert body["description"] == "keep me"       # unchanged
    assert body["rollout_percentage"] == 20        # unchanged


def test_delete_flag(client):
    client.post("/flags", json={"key": "delete-me"})
    response = client.delete("/flags/delete-me")
    assert response.status_code == 204

    follow_up = client.get("/flags/delete-me")
    assert follow_up.status_code == 404


def test_delete_nonexistent_flag_returns_404(client):
    response = client.delete("/flags/never-existed")
    assert response.status_code == 404
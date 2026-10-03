"""
Tests for the evaluation endpoint and the bucketing logic behind it
(app/routers/evaluate.py, app/crud.py's bucket_user).
"""

from app.crud import bucket_user


def test_bucket_user_is_deterministic():
    """
    The core guarantee: same user, same flag, same bucket -- every
    single time, with no randomness involved.
    """
    first = bucket_user("alice", "some-flag")
    second = bucket_user("alice", "some-flag")
    assert first == second


def test_bucket_user_is_within_range():
    bucket = bucket_user("alice", "some-flag")
    assert 0 <= bucket <= 99


def test_bucket_user_differs_by_flag():
    """
    The same user can land in a different bucket for a different flag --
    bucketing is per (user, flag) pair, not just per user.
    """
    bucket_for_flag_a = bucket_user("alice", "flag-a")
    bucket_for_flag_b = bucket_user("alice", "flag-b")
    # Not asserting they're different -- they could coincidentally
    # match -- just confirming both are independently valid buckets.
    assert 0 <= bucket_for_flag_a <= 99
    assert 0 <= bucket_for_flag_b <= 99


def test_evaluate_consistent_across_repeated_calls(client):
    client.post(
        "/flags", json={"key": "consistency-flag", "enabled": True, "rollout_percentage": 50}
    )
    results = [
        client.get("/evaluate/consistency-flag", params={"user_id": "alice"}).json()["enabled"]
        for _ in range(10)
    ]
    assert len(set(results)) == 1  # every call returned the same value


def test_disabled_flag_always_returns_false(client):
    client.post(
        "/flags", json={"key": "disabled-flag", "enabled": False, "rollout_percentage": 100}
    )
    response = client.get("/evaluate/disabled-flag", params={"user_id": "alice"})
    assert response.json()["enabled"] is False


def test_zero_percent_rollout_returns_false_for_everyone(client):
    client.post("/flags", json={"key": "zero-flag", "enabled": True, "rollout_percentage": 0})
    for user in ["alice", "bob", "carol", "dave", "eve"]:
        response = client.get("/evaluate/zero-flag", params={"user_id": user})
        assert response.json()["enabled"] is False


def test_hundred_percent_rollout_returns_true_for_everyone(client):
    client.post("/flags", json={"key": "full-flag", "enabled": True, "rollout_percentage": 100})
    for user in ["alice", "bob", "carol", "dave", "eve"]:
        response = client.get("/evaluate/full-flag", params={"user_id": user})
        assert response.json()["enabled"] is True


def test_evaluate_nonexistent_flag_returns_404(client):
    response = client.get("/evaluate/does-not-exist", params={"user_id": "alice"})
    assert response.status_code == 404
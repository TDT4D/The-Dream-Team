"""
Tests for the /score/scores endpoint of the ML API.

Covers:
- Retrieving all scores from file
- Filtering scores by projectId
- 404 errors for missing scores or unmatched projectId
- 500 internal error when loading scores fails

Mocks:
- storage.load_json(): returns fake score data, empty lists, or raises exceptions
- Uses `load_test_json()` to load test score data

Note:
- projectId is optional; if not provided, all scores are returned
"""



from fastapi.testclient import TestClient
from api.main import app
from utils.testing_utils import load_test_json

client = TestClient(app)

def fake_load_json_success(*args, **kwargs):
    return load_test_json("test_score_data.json")

def fake_load_json_empty(*args, **kwargs):
    return []

def filtered_scores(*args, **kwargs):
        return [
            {"projectId": 42, "studentId": 101, "Score": 0.87},
            {"projectId": 42, "studentId": 102, "Score": 0.76},
            {"projectId": 5, "studentId": 201, "Score": 0.91}
        ]


def test_get_scores_success(monkeypatch):
    monkeypatch.setattr("api.routers.prediction.storage.load_json", fake_load_json_success)

    response = client.get("/score/scores", params={
        "scoreFile": "some_data"
    })

    assert response.status_code == 200
    assert "scores" in response.json()

def test_get_scores_with_project_id(monkeypatch):
    monkeypatch.setattr("api.routers.prediction.storage.load_json", filtered_scores)

    response = client.get("/score/scores", params={
        "projectId": 42,
        "scoreFile": "some_data"
    })

    assert response.status_code == 200
    scores = response.json()["scores"]
    assert all(score["studentId"] in [101, 102] for score in scores)
    assert "projectId" not in scores[0]

def test_get_scores_with_wrong_id(monkeypatch):
    monkeypatch.setattr("api.routers.prediction.storage.load_json", filtered_scores)

    response = client.get("/score/scores", params={
        "projectId": 999,
        "scoreFile": "some_data"
    })

    assert response.status_code == 404
    assert "No scores found for projectId" in response.json().get("error", "")

def test_scores_not_found(monkeypatch):
    monkeypatch.setattr("api.routers.prediction.storage.load_json", fake_load_json_empty)

    response = client.get("/score/scores", params={
        "scoreFile": "some_data"
    })

    assert response.status_code == 404
    assert "No scores found" in response.json().get("error", "")

def test_scores_not_found_for_project(monkeypatch):
    monkeypatch.setattr("api.routers.prediction.storage.load_json", fake_load_json_empty)

    response = client.get("/score/scores", params={
        "projectId": 999,
        "scoreFile": "some_data"
    })

    assert response.status_code == 404
    assert "No scores found for projectId" in response.json().get("error", "")

def test_get_scores_exception(monkeypatch):
    monkeypatch.setattr("api.routers.prediction.storage.load_json", lambda _: (_ for _ in ()).throw(Exception("error occured")))

    response = client.get("/score/scores", params={
        "scoreFile": "APIscore"
    })

    assert response.status_code == 500
    assert "unexpected error occurred" in response.json().get("error", "").lower()
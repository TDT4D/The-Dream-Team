"""
Tests for the /team/build-team endpoint of the ML API.

Covers:
- Team building success with valid input
- Handling of empty or invalid team data
- Error handling when team builder raises an exception

Mocks:
- team_builder.build_team(): returns a mocked team or raises an error
- Uses simulated score data as return values

Note:
- Designed to be compatible with future modular team builder (get_team_builder)
"""



from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)

def fake_team_builder_success(size, projectId, data, saveFile):
    return {
        "projectId": projectId,
        "team": [
            {"studentId": 1, "Score": 95.0},
            {"studentId": 2, "Score": 92.5},
        ]
    }

def fake_team_builder_empty(size, projectId, data, saveFile):
    return {
        "projectId": projectId,
        "team": []
    }

def fake_team_builder_exception(size, projectId, data, saveFile):
    raise Exception("Something went wrong in team building")


def test_team_build_success(monkeypatch):
    monkeypatch.setattr("api.routers.team_building.team_builder.build_team", fake_team_builder_success)

    response = client.post("/team/build-team", params={
        "projectId": 101,
        "size": 2,
        "data": "some_data",
        "saveFile": "test_team"
    })

    assert response.status_code == 200
    data = response.json()
    assert "team" in data
    assert len(data["team"]) == 2
    assert "studentId" in data["team"][0]

def test_team_build_empty(monkeypatch):
    monkeypatch.setattr("api.routers.team_building.team_builder.build_team", fake_team_builder_empty)

    response = client.post("/team/build-team", params={
        "projectId": 101,
        "size": 2,
        "data": "APIscore",
        "saveFile": "APIteam"
    })

    assert response.status_code == 400
    assert "No valid team members" in response.json().get("error", "")

def test_team_build_exception(monkeypatch):
    monkeypatch.setattr("api.routers.team_building.team_builder.build_team", fake_team_builder_exception)

    response = client.post("/team/build-team", params={
        "projectId": 101,
        "size": 2
    })

    assert response.status_code == 500
    assert "unexpected error" in response.json().get("error", "").lower()
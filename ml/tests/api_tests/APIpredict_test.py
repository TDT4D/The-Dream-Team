"""
Tests for the /score/predict endpoint of the ML API.

Covers:
- Prediction with valid inputs and mocked model
- Model name validation logic
- Prediction failure scenario (model returns None)
- Exception handling during model prediction

Mocks:
- get_model(): returns a fake model object with .predict method
- Uses `load_test_json()` to simulate score outputs

Note:
- Assumes default values for modelType and modelName are valid
"""



from fastapi.testclient import TestClient
from api.main import app
from utils.testing_utils import load_test_json

client = TestClient(app)

def fake_predict_success(*args, **kwargs):
    return load_test_json("test_score_data.json")

def fake_predict_none(*args, **kwargs):
    return None

def fake_predict_exception(*args, **kwargs):
    raise Exception("Something went wrong")

def fake_data_empty(*args, **kwargs):
    return []


def test_predict_success(monkeypatch):
    monkeypatch.setattr("api.routers.prediction.get_model", lambda name: type("FakeCleaner", (), {
    "predict": fake_predict_success
    })())

    response = client.post("/score/predict", params={
        "modelType": "randomforest_v2",
        "modelName": "randomforest_v2_API",
        "data": "some_data",
        "cleaning": False,
        "saveFile": "test_scored"
    })

    assert response.status_code == 200
    assert "Prediction and scoring completed successfully" in response.json().get("message", "")


def test_predict_model_validation_fail():
    response = client.post("/score/predict", params={
        "modelType": "randomforest_v2",
        "modelName": "svm_model"  # doesn't match
    })
    assert response.status_code == 400
    assert "does not match model type" in response.text


def test_predict_returns_none(monkeypatch):
    monkeypatch.setattr("api.routers.prediction.get_model", lambda name: type("FakeModel", (), {
        "predict": fake_predict_none
    })())

    response = client.post("/score/predict", params={
        "modelType": "randomforest_v2",
        "modelName": "randomforest_v2_API",
        "data": "some_data",
        "saveFile": "test_scored"
    })

    assert response.status_code == 400
    assert "Scores are" in response.json().get("error", "")


def test_predict_raises_exception(monkeypatch):
    monkeypatch.setattr("api.routers.prediction.get_model", lambda name: type("FakeModel", (), {
        "predict": fake_predict_exception
    })())

    response = client.post("/score/predict", params={
        "modelType": "randomforest_v2",
        "modelName": "randomforest_v2_API"
    })

    assert response.status_code == 500
    assert "An error occurred" in response.json().get("error", "")
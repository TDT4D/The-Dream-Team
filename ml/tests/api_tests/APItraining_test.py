from fastapi.testclient import TestClient
from api.main import app
from utils.testing_utils import load_test_json

client = TestClient(app)

def test_training_success(monkeypatch):
    """
    def fake_train(self, data, model_name, cleaning):
        print("FAKE TRAIN CALLED")
        print("DATA:", data)
        print("MODEL_NAME:", model_name)
        print("CLEANING:", cleaning)

        assert isinstance(data, list), "Expected cleaned data to be a list"
        assert data and isinstance(data[0], dict), "Expected list of dicts"
        return True
    
    def fake_clean_data(self, load_name, save_name):
        print(f"FAKE CLEAN DATA CALLED with: {load_name=} {save_name=}")
        data = load_test_json("test_cleaned_data.json")
        print("Loaded data from JSON:", data[:1])  # Just a preview
        return data
    """

    def fake_train(*args, **kwargs):
        return True
    
    def fake_clean_data(*args, **kwargs):
        data = load_test_json("test_cleaned_data.json")
        return data

    monkeypatch.setattr("api.routers.training.get_model", lambda name: type("FakeModel", (), {
    "train": fake_train
    })())
    monkeypatch.setattr("api.routers.training.get_cleaner", lambda name: type("FakeCleaner", (), {
    "clean_data": fake_clean_data
    })())

    response = client.post("/training/train", params={
        "modelType": "randomforest_v2",
        "modelName": "randomforest_v2_test",
        "data": "some_data",
        "cleaning": True
    })

    assert response.status_code == 200
    assert "Model trained successfully" in response.json().get("message", "")


def test_training_invalid_model_name():
    response = client.post("/training/train", params={
        "modelType": "randomforest_v2",
        "modelName": "svm_model",  #Does not match
    })
    assert response.status_code == 400

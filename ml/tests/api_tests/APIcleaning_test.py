"""
Tests for the /data/clean endpoint of the ML API.

Covers:
- Successful data cleaning with valid data
- Handling of empty data (empty list or list of empty dicts)
- Proper response when no data is returned (None)
- Error handling when the cleaner raises an exception

Mocks:
- get_cleaner(): Returns a FakeCleaner with a custom clean_data method
- Uses load_test_json to simulate file-based test data

Behavior:
- Valid cleaned data ➜ 200 OK with "Data cleaned successfully"
- Empty or unusable cleaned data ➜ 200 OK with special warning message
- None (missing data) ➜ 400 Bad Request
- Internal exception ➜ 500 Server Error
"""


from fastapi.testclient import TestClient
from api.main import app
from utils.testing_utils import load_test_json

client = TestClient(app)


def fake_clean_data_success(*args, **kwargs):
    return load_test_json("test_cleaned_data.json")

def fake_clean_data_empty(*args, **kwargs):
    return []

def fake_clean_data_empty_file(*args, **kwargs):
    return load_test_json("test_empty_data.json")

def fake_clean_data_none(*args, **kwargs):
    return None

def raise_exception(*args, **kwargs):
    raise Exception("Something went wrong")

def test_cleaning_success(monkeypatch):
    monkeypatch.setattr("api.routers.cleaning.get_cleaner", lambda name: type("FakeCleaner", (), {
    "clean_data": fake_clean_data_success
    })())

    response = client.post("/data/clean", params={
        "data": "some_data",
        "cleaner": "default_cleaner",
        "saveFile": "test_cleaned"
    })

    assert response.status_code == 200

    json_data = response.json()
    assert json_data["message"] == "Data cleaned succesfully"
    assert "data" in json_data
    assert isinstance(json_data["data"], list)

    sample = json_data["data"][0]
    assert "projectId" in sample
    assert "studentId" in sample

def test_cleaning_empty(monkeypatch):
    monkeypatch.setattr("api.routers.cleaning.get_cleaner", lambda name: type("FakeCleaner", (), {
        "clean_data": fake_clean_data_empty
    })())

    response = client.post("/data/clean", params={
        "data": "some_data",
        "cleaner": "default_cleaner",
        "saveFile": "test_cleaned"
    })

    assert response.status_code == 200

    json_data = response.json()
    assert json_data.get("data") == []
    assert "no usable data found" in json_data.get("message", "").lower()

def test_cleaning_empty_file(monkeypatch):
    monkeypatch.setattr("api.routers.cleaning.get_cleaner", lambda name: type("FakeCleaner", (), {
        "clean_data": fake_clean_data_empty_file
    })())

    response = client.post("/data/clean", params={
        "data": "some_data",
        "cleaner": "default_cleaner",
        "saveFile": "test_cleaned"
    })

    assert response.status_code == 200

    json_data = response.json()
    assert isinstance(json_data.get("data"), list)
    assert all(not row for row in json_data["data"])  # all rows empty
    assert "no usable data found" in json_data.get("message", "").lower()


def test_cleaning_none(monkeypatch):
    monkeypatch.setattr("api.routers.cleaning.get_cleaner", lambda name: type("FakeCleaner", (), {
        "clean_data": fake_clean_data_none
    })())

    response = client.post("/data/clean", params={
        "data": "some_data",
        "cleaner": "default_cleaner",
        "saveFile": "test_cleaned"
    })

    assert response.status_code == 400
    assert "ValueError" in response.json().get("error", "")


def test_cleaning_exception(monkeypatch):
    monkeypatch.setattr("api.routers.cleaning.get_cleaner", lambda name: type("FakeCleaner", (), {
        "clean_data": raise_exception
    })())

    response = client.post("/data/clean", params={
        "data": "test_raw_data"
    })

    assert response.status_code == 500
    assert "An error occurred while cleaning data" in response.json().get("error", "")
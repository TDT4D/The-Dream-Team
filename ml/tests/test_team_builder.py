import pytest
from team_building.team_builder import build_team
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


"""

"""
@pytest.fixture
def mock_data():
    return [
        {"projectId": 998, "studentId": 1, "Score": 95.0},
        {"projectId": 998, "studentId": 2, "Score": 90.0},
        {"projectId": 998, "studentId": 3, "Score": 85.0},
        {"projectId": 1046, "studentId": 4, "Score": 80.0},
    ]

# A scenario with valid values, should succeed
def test_build_team_success(mocker, mock_data):
    mocker.patch("team_building.team_builder.storage.load_json", return_value=mock_data)
    mock_save = mocker.patch("team_building.team_builder.storage.save_json")  


    result = build_team(n=2)

    assert result == {
        "projectId": 998,
        "team": [
            {"projectId": 998, "studentId": 1, "Score": 95.0},
            {"projectId": 998, "studentId": 2, "Score": 90.0},
        ],
    }
    mock_save.assert_called_once_with(result, "team_example")

# A scenario with a lower number of students than n
def test_build_team_fewer_students(mocker, mock_data):
    mocker.patch("team_building.team_builder.storage.load_json", return_value=mock_data)
    mock_save = mocker.patch("team_building.team_builder.storage.save_json")


    result = build_team(n=10)

    assert result == {
        "projectId": 998,
        "team": [
            {"projectId": 998, "studentId": 1, "Score": 95.0},
            {"projectId": 998, "studentId": 2, "Score": 90.0},
            {"projectId": 998, "studentId": 3, "Score": 85.0},
        ],
    }
    mock_save.assert_called_once_with(result, "team_example")

# a scenario where no matching projectId is found
def test_build_team_no_matching_project(mocker, mock_data):
    mocker.patch("team_building.team_builder.storage.load_json", return_value=mock_data)
    mock_save = mocker.patch("team_building.team_builder.storage.save_json")

    result = build_team(n=2, project_id=999)

    assert result == {"projectId": 999, "team": []}
    mock_save.assert_not_called()

# A scenario where the input data is not a list
def test_build_team_invalid_data_format(mocker):
    mocker.patch("team_building.team_builder.storage.load_json", return_value=mock_data)
    
    result = build_team(n=2)
    
    assert result is None

# A scenario where the dataset is empty
def test_build_team_empty_data(mocker):
    """Test that an empty JSON file results in an empty team."""
    mocker.patch("team_building.team_builder.storage.load_json", return_value=[])

    result = build_team(3, project_id=998)
    assert result == {"projectId": 998, "team": []}

def test_build_team_invalid_n(mocker):
    """Test that invalid values of `n` raise an error or return an empty team."""
    mock_data = [
        {"projectId": 998, "studentId": 1, "Score": 90.0},
        {"projectId": 998, "studentId": 2, "Score": 85.0}
    ]
    mocker.patch("team_building.team_builder.storage.load_json", return_value=mock_data)

    # Negative n should return an empty team
    result = build_team(-1, project_id=998)
    assert isinstance(result["team"], list)

    # Zero n should return an empty team
    result = build_team(0, project_id=998)
    assert result == {"projectId": 998, "team": []}

    # Non-integer n should raise a TypeError
    with pytest.raises(TypeError):
        build_team("five", project_id=998)

def test_build_team_invalid_project_id(mocker):
    """Test that invalid `project_id` values handle correctly."""
    mock_data = [
        {"projectId": 998, "studentId": 1, "Score": 90.0}
    ]
    mocker.patch("team_building.team_builder.storage.load_json", return_value=mock_data)

    result = build_team(2, project_id="abc")
    assert result == {"projectId": "abc", "team": []}

def test_build_team_missing_fields(mocker):
    """Test that missing fields in input raise a KeyError (if unhandled)."""
    mock_data = [
        {"projectId": 998, "studentId": 1},  # Missing "Score"
        {"studentId": 2, "Score": 85.0}      # Missing "projectId"
    ]
    mocker.patch("team_building.team_builder.storage.load_json", return_value=mock_data)

    with pytest.raises(KeyError):
        build_team(3, project_id=998)

def test_build_team_returns_dict(mocker):
    """Test that the return type of `build_team()` is always a dictionary."""
    mock_data = [
        {"projectId": 998, "studentId": 1, "Score": 95.0},
        {"projectId": 998, "studentId": 2, "Score": 90.0}
    ]
    mocker.patch("team_building.team_builder.storage.load_json", return_value=mock_data)

    result = build_team(2, project_id=998)
    assert isinstance(result, dict)

    result = build_team(2, project_id=998)
    assert isinstance(result, dict)

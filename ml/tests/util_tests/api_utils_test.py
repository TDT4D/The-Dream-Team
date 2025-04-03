"""
Tests for utils/api_utils.py.

Covers:
- Model name validation logic for consistency between model type and name

Function tested:
- validate_model(): ensures modelName starts with modelType
"""


from utils.api_utils import validate_model


def test_validate_model_success():
    assert validate_model("randomforest_v2", "randomforest_v2_test") is True
    assert validate_model("svm", "svm_model_v1") is True


def test_validate_model_failure():
    assert validate_model("randomforest_v2", "svm_model") is False
    assert validate_model("svm", "model_svm") is False
    assert validate_model("xgboost", "boostxg_model") is False

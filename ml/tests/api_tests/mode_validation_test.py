from api.routers.training import validate_model

def test_validate_model_success():
    assert validate_model("randomforest_v2", "randomforest_v2_test")

def test_validate_model_failure():
    assert not validate_model("randomforest_v2", "xgboost_test")

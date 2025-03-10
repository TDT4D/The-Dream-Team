from fastapi import APIRouter, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from models import get_model
from data_handling import get_cleaner

router = APIRouter()

def validate_model(model_type:str, model_name:str) -> bool:
    """
    Validates that the model_name matches the expected model_type.
    - ModelName must start with (and include) modelType
    Args:
        model_type (str): The type of the model (e.g., "randomforest_v2").
        model_name (str): The name of the saved model (e.g., "randomforest_v2_test").

    Returns:
        bool: True if valid, False otherwise.
    """
    return model_name.startswith(f"{model_type}")

@router.post("/train")
def start_training(
    background_tasks: BackgroundTasks,
    modelType: str = Query(default="randomforest_v2", description="Type of the used model"),
    modelName: str = Query(default="randomforest_v2_API", description="Name of the saved model"),
    data: str = Query(default="clean_v3_modular_test", description="Data file name"),
    cleaning: bool = Query(default=False, description="Does the data require cleaning")
):
    """
    Trains a new model of specified type and saves it with the given modelName.

    - Cleans data if necessary
    - Validates the modenType and modelName
    - Trains a new model of the type
    - Saves the model with modelName to /data/saved_models

    Args:
        model_type (str): Type of the used model
        model_name (str): The saved model used for prediction (default: "")
        data (str): Name of the raw data file to process
        cleaning (bool): Check if cleaning is needed (uses default cleaner)

    Returns:
        JSONResponse: Success or error message
    """

    #train(data="rawData", model_name="randomforest_v2", cleaning:bool=True)

    if not validate_model(modelType, modelName):
        return JSONResponse(
            status_code=400,
            content={"error": f"Model name '{modelName}' does not match model type '{modelType}'"}
        )

    #Clean data here if necessary
    if cleaning:
        data = get_cleaner("default_cleaner").clean_data(data, "trainAPI_clean")
        print("Data cleaned, ready for training")

    try:
        model = get_model(modelType)
        confirmation = model.train(data=data, model_name=modelName, cleaning=False)
        if confirmation:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Model trained successfully",
                    "savedFile": f"{modelName}.joblib"
                }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "message": "Model training/saving unsuccessfull",
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred while traing model: {str(e)}"}
        )
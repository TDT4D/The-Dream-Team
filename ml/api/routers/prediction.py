from fastapi import APIRouter, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from data_handling import data_cleaning
from models import random_forest

router = APIRouter()

@router.post("/predict")
def start_prediction(
    background_task: BackgroundTasks,
    model: str = Query(default="randomforest_v2", description="Model to use for predictions"),
    data: str = Query(default="rawData", description="Raw data file name"),
    saveFile: str = Query(default="score_api_v1", description="Name of the file to save scores")
):
    """
    Generates a score file from cleaned data.

    - Cleans rawData
    - Generates scores from cleaned data  using selected model
    - BackgroundTask not implemented

    Args:
        model (str): The model used for prediction (default: "randomforest_v2")
        data (str): Name of the raw data file to process
        saveFile (str): Name of the file where scores are stored

    Returns:
        JSONResponse: Success or error message
    """
    try:
        #Clean raw data
        cleaned_data = data_cleaning.clean_data_v2(data, "cleaned_api")

        if not cleaned_data:
            return JSONResponse(
                status_code=400, 
                content={"error": "raw data could not be cleaned"}
            )
        
        #Generate and save scores
        random_forest.randomforest_v2(cleaned_data, saveFile, False)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Prediction and scoring completed successfully",
                "savedFile": f"{saveFile}.json"
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )

    #return {"message:" "prediction and scoring not implemented"}


@router.get("/scores")
def get_scores(
    projectId: int | None = Query(default=None, description="ID of the project to fetch scores for")

):
    """
    Fetches scores for a specific project if projectId is provided,
    otherwise fetches all scores

    Args:
        projectId (int): id for project which scores are wanted
                         default=None: returns all scores

    Returns:
        dict: A list of scores.

    """

    if projectId:
        return {"message": f"fetching scores for {projectId} not implemented"}
    return {"message": "fetching scores not implemented"}

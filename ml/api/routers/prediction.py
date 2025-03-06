from fastapi import APIRouter, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from data_handling import data_cleaning
from models import get_model
from utils import storage
from typing import Optional

router = APIRouter()


def validate_model(model_type:str, model_name:str) -> bool:
    """
    Validates that the model_name matches the expected model_type.

    Args:
        model_type (str): The type of the model (e.g., "randomforest").
        model_name (str): The name of the saved model (e.g., "randomforest_v1").

    Returns:
        bool: True if valid, False otherwise.
    """
    return model_name.startswith(f"{model_type}_")

#Should Work
@router.post("/predict")
def start_prediction(
    background_task: BackgroundTasks,
    model_type: str = Query(default="randomforest_v2", description="Type of the used model"),
    model_name: str = Query(default="", description="Name of the saved model"),
    data: str = Query(default="clean_v3_modular_test", description="Data file name"),
    cleaning: bool = Query(default=False, description="Does the data require cleaning"),
    saveFile: str = Query(default="score_api_v1", description="File name to save scores")
):
    """
    Generates a score file from data.

    - Checks if model type and name match (prevents missmatch errors)
    - Generates scores from cleaned data using selected model
    - BackgroundTask not implemented

    Args:
        model_type (str): Type of the used model
        model_name (str): The saved model used for prediction (default: "")
        data (str): Name of the raw data file to process
        cleaning (bool): Check if cleaning is needed (uses default cleaner)
        saveFile (str): Name of the file where scores are stored

    Returns:
        JSONResponse: Success or error message
    """

    if not validate_model(model_type, model_name):
        return JSONResponse(
            status_code=400,
            content={"error": f"Model name '{model_name}' does not match model type '{model_type}.'"}
        )

    try:

        #Generate and save scores
        model = get_model(model_type)
        model.predict(data, model_name, saveFile, cleaning)

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
    projectId: Optional[int] = Query(default=None, description="ID of the project to fetch scores for"),
    scoreFile: str = Query(default="score_api_v1", description="Name of the score file")

):
    """
    Fetches student scores
    - Fetches for specific project if ID given
    - Else fetches all scores

    Args:
        projectId (int, optional): ID of the project for which scores are required.
                                   If None, returns all scores.
        scoreFile (str): Name of the score file to fetch scores from (default: "score_api_v1")

    Returns:
        JSONResponse: List of scores or an error message.

    """

    try:
        #Load scores
        scores = storage.load_json(scoreFile)

        #Filter by projectId if provided
        if projectId is not None:
            filtered_scores = [entry for entry in filtered_scores if entry.get("projectId") == projectId]
            if not filtered_scores:
                return JSONResponse(
                    status_code=404,
                    content={"error": f"No scores found for projectId {projectId}"}
                )
            
            #Filter to only include studentId, score
            filtered_scores = [
                {"studentId": entry["studentId"], "Score": entry["Score"]}
                for entry in filtered_scores
            ]

            return JSONResponse(
                status_code=200,
                content={"projectId": projectId, "scores": filtered_scores}
            )
        

        #Filter to only include projectId, studentId, score
        filtered_scores = [
            {"projectId": entry["projectId"], "studentId": entry["studentId"], "Score": entry["Score"]}
            for entry in scores
        ]

        #Return all scores if no projectId is provided
        return JSONResponse(
            status_code=200,
            content={"scores": filtered_scores}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An unexpected error occurred: {str(e)}"}
        )

    #if projectId:
    #    return {"message": f"fetching scores for {projectId} not implemented"}
    #return {"message": "fetching scores not implemented"}

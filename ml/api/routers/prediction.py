from fastapi import APIRouter, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from data_handling import data_cleaning
from models import get_model
from utils import storage
from typing import Optional

router = APIRouter()

#Should Work
@router.post("/predict")
def start_prediction(
    background_task: BackgroundTasks,
    model_name: str = Query(default="randomforest_v2", description="Model to use for predictions"),
    data: str = Query(default="rawData", description="Raw data file name"),
    saveFile: str = Query(default="score_api_v1", description="Name of the file to save scores")
):
    """
    Generates a score file from cleaned data.

    - Expects clean data
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

        #Generate and save scores
        model = get_model(model_name)
        model(data, model_name, saveFile, False)

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

#Doesn't fully work
@router.post("/raw_predict")
def start_c_prediction(
    background_task: BackgroundTasks,
    model_name: str = Query(default="randomforest_v2", description="Model to use for predictions"),
    data: str = Query(default="rawData", description="Raw data file name"),
    cleaner: str = Query(default="clean_data_v2", description="Cleaning method"),
    saveFile: str = Query(default="score_api_v1", description="Name of the file to save scores")
):
    """
    Generates a score file from raw data.

    - Cleans rawData
    - Generates scores from cleaned data using selected model
    - BackgroundTask not implemented

    Args:
        model (str): The model used for prediction (default: "randomforest_v2")
        data (str): Name of the raw data file to process
        cleaner (str): Name of the method used to clean raw data
        saveFile (str): Name of the file where scores are stored

    Returns:
        JSONResponse: Success or error message
    """
    try:
        #Clean raw data //TODO
        cleaned_data = data_cleaning.get_cleaner(data, "cleaned_api")

        if not cleaned_data:
            return JSONResponse(
                status_code=400, 
                content={"error": "raw data could not be cleaned"}
            )
        

        #predict(data="rawData", model_name="randomforest_v2", score_name="student_scores_default", cleaning:bool=True)
        #Generate and save scores
        model = get_model(model_name)
        get_model(model_name)(cleaned_data, model_name, saveFile, False)

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

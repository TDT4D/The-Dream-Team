from fastapi import APIRouter, BackgroundTasks
from typing import Optional
import logging

router = APIRouter()

@router.post("/predict")
def start_prediction(background_task: BackgroundTasks):
    """Starts predicting scores"""
    return {"message:" "prediction and scoring not implemented"}


@router.get("/scores")
def get_scores(projectId: Optional[int] = None):
    """
    Fetches scores from database (placeholder, might not be used)

    Args:
        projectId (int): id for project which scores are wanted
        default None: returns all scores

    Returns:
        dict: A list of scores.

    """
    logging.info(f"Received project id {projectId}")
    print(f"Received projectId: {projectId}")
    if projectId:
        return {"message": f"fetching scores for {projectId} not implemented"}
    return {"message": "fetching scores not implemented"}

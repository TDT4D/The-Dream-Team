from fastapi import APIRouter, BackgroundTasks, Query


router = APIRouter()

@router.post("/predict")
def start_prediction(background_task: BackgroundTasks):
    """Starts predicting scores"""
    return {"message:" "prediction and scoring not implemented"}


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

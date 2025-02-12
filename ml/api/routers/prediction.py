from fastapi import APIRouter, BackgroundTasks

router = APIRouter()

@router.post("/predict")
def start_prediction(background_task: BackgroundTasks):
    """Starts predicting scores"""
    return {"message:" "prediction and scoring not implemented"}


@router.get("/scores")
def get_scores():
    """Fetches all scores from database (placeholder, might not be used)"""
    return {"message:" "fetching scores not implemented"}

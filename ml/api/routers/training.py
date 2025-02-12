from fastapi import APIRouter, BackgroundTasks

router = APIRouter()

@router.post("/train")
def start_training(background_tasks: BackgroundTasks):
    """Starts training a new model"""
    return {"message:" "Training not implemented"}
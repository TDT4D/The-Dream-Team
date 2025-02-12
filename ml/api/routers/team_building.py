from fastapi import APIRouter

router = APIRouter()

@router.post("/build-team")
def build_team():
    """Builds the team based on stored predictions/scores"""
    return {"message:" "Team building not implemented"}

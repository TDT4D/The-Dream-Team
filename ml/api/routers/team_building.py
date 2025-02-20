from fastapi import APIRouter

router = APIRouter()

@router.post("/build-team")
def build_team(projectId: int):
    """
    Builds the team based on stored predictions/scores

     Args:
        projectId (int): id for project

    Returns:
        dict: A list of team members.
    """
    print(f"Received projectId: {projectId}")
    
    return {"message:" "Team building not implemented"}

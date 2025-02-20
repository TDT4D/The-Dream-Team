from fastapi import APIRouter, Query

router = APIRouter()

@router.post("/build-team")
def build_team(
    projectId: int = Query(description="ID of the project to fetch scores for"),
    size: int = Query(default=5, description="Number of team members")
):
    """
    Builds the team based on stored predictions/scores

     Args:
        projectId (int): id for project
        size (ing): size of the team, default=5

    Returns:
        dict: A list of team members.
    """
    #print(f"Received projectId: {projectId}")

    return {"message:" f"Team building not implemented || received projectId: {projectId} and size: {size}"}

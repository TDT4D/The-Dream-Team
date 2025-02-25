from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from team_building import team_builder

router = APIRouter()

@router.post("/build-team")
def build_team(
    projectId: int = Query(description="ID of the project to fetch scores for"),
    size: int = Query(default=5, description="Number of team members"),
    data: str = Query(default="student_score_example", description="Name of the score file")
):
    """
    Builds the team based on stored predictions/scores

     Args:
        projectId (int): id for project
        size (ing): size of the team, default=5

    Returns:
        dict/json response: A list of team members.
    """
    #print(f"Received projectId: {projectId}")

    try:
        team_data = team_builder.build_team(size, data)
        if not team_data["team"]:
            return JSONResponse(
            status_code = 400,
            content={"error": "No valid team members found. Check data"}
            )
        return JSONResponse(
            status_code=200,
            content={"projectId": projectId, "team":team_data["team"]}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An unexpected error occured: {str(e)}"}
        )

    #return {"message:" f"Team building not implemented || received projectId: {projectId} and size: {size}"}

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from team_building import team_builder

router = APIRouter()

@router.post("/build-team")
def build_team(
    projectId: int = Query(description="ID of the project to fetch scores for"),
    size: int = Query(default=5, description="Number of team members"),
    data: str = Query(default="score_v1", description="Name of the score file"),
    saveFile: str = Query(default="team_v1", description="Name of the file team is saved")
):
    """
    Builds the team based on stored predictions/scores

     Args:
        projectId (int): id for project
        size (int): size of the team, default=5
        data (string): Name of the score file
        saveFile (String): Name of the file team is saved

    Returns:
        JSONResponse: A list of team members.


    Expected return format:

    {
        "projectId": 1046,
        "team": 
        [
            {
                "studentId": 21975,
                "Score": 100.0
            },
            {
                "studentId": 22044,
                "Score": 100.0
            }
        ]
    }

    """
    #print(f"Received projectId: {projectId}")

    """n projectId loadName saveName"""

    try:
        #Builds and saves team
        team_data = team_builder.build_team(size, projectId, data, saveFile)

        if not team_data.get("team"):
            return JSONResponse(
            status_code = 400,
            content={"error": "No valid team members found. Check data"}
            )
        
        #Extract only studentId and Score
        filtered_team = [
            {"studentId": member["studentId"], "Score": member["Score"]}
            for member in team_data["team"]
        ]

        return JSONResponse(
            status_code=200,
            content={"projectId": projectId, "team": filtered_team}
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An unexpected error occured: {str(e)}"}
        )

    #return {"message:" f"Team building not implemented || received projectId: {projectId} and size: {size}"}

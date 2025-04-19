from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from team_building import team_builder
from typing import Optional
from team_building import get_team_builder


router = APIRouter()

@router.post("/build-team")
def build_team(
    projectId: int = Query(description="ID of the project to fetch scores for"),
    size: int = Query(default=5, description="Number of team members"),
    data: str = Query(default="APIscore", description="Name of the score file"),
    saveFile: str = Query(default="APIteam", description="Name of the file team is saved")
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

@router.post("/dream-team")
def dream_team(
    applicants: str = Query(..., description="Data of applicants"),
    scores: str = Query(..., description="Data of applicant scores"),
    motivations: str = Query(..., description="Data of applicant motivation"),
    team_size: int = Query(default=4, description="Number of team members"),
    save_file: str = Query(default="dreamteam", description="Number of team members"),
    projectId: Optional[int] = Query(default=None, description="Team building for single project")
):
    
    """
    Builds the Dream Team

    - **If `projectId` is provided:**
        - Team suggestions for a single project
        - **Returns:**
        
            {
            "best_overall": best_team, #average teams score highest
            "perfect_team": perfect_team, #Individual scores are highest
            "diverse_teams": diverse_teams[:3],  #top 3 diverse suggestions
            "all_teams": valid_teams  #All valid teams
            }

    - **Otherwise (no `projectId`):**
        - Gives suggestions for all teams
        - **Return:**
        list of suggested teams for all projects:
            {
                "teams": final_teams for all projects that have valid teams
                "project_failure_reasons": Justifications why project doesn't have a team
            }


            - **`final_teams` structure:**
            [
                {
                    "projectId": 1047.0,
                    "team": [
                        {
                            "projectId": 1047.0,
                            "studentId": 21816.0,
                            "whyProject": 0.5065285563468933,
                            "whyExperience": 0.37186917662620544,
                            "location_match": 2.0,
                            "field": 12,
                            "score": 71.91999053955078,
                            "motivation_score": 84.96797180175781,
                            "final_score": 68.04236508607865,
                            "justification":...
                        },...
                    ],
                    "avg_score": 64.25695798993111,
                    "justification": [
                        "Team includes students from 4 unique fields."
                    ]
                },
            ]
    
    """

    try:
        
        builder = get_team_builder("dreamteam_builder")

        if projectId is None:
            dream_team = builder.build_team(
                team_size=team_size, 
                applicant_data=applicants, 
                score_data=scores, 
                motivation_score=motivations, 
                save_name=save_file
            )
        else:
            dream_team = builder.build_team(
                project_id=projectId,
                team_size=team_size, 
                applicant_data=applicants, 
                score_data=scores, 
                motivation_score=motivations, 
                save_name=save_file
            )

        if not dream_team:
            raise ValueError("Error while building the dream team.")

        return JSONResponse(
            status_code=200,
            content=dream_team
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An unexpected error occured: {str(e)}"}
        )



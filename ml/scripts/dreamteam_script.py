from team_building import dreamteam_builder
import json

#called from The-Dream-Team\ml>python -m scripts.team_test


#print("Begin team building")

#dreamteam_builder.build_team()

teams = dreamteam_builder.build_team(project_id=1060)

print("Teams::::::::::::::::\n")

if teams is not None:
    print("\nBest team")
    print(json.dumps(teams['best_overall'], indent=4))
    print("\nPerfect team")
    print(json.dumps(teams['perfect_team'], indent=4))
    print("\nDiverse teams")
    for i, team in enumerate(teams['diverse_teams'], start=1):
        print(f"\nDiverse Team {i}:")
        print(json.dumps(team, indent=4))
    
    print("\nAll valid teams:")
    most = teams['all_teams'][:2]
    print(f"total teams: {len(teams['all_teams'])}")
    for i, team in enumerate(most, start=1):
        print(f"\nValid Team {i}:")
        print(json.dumps(team, indent=4))

else:
    print(f"NO TEAMS, teams = {teams}")

"""
    Team compositions
    {
        "best_overall": best_team, #average teams score highest
        "perfect_team": perfect_team, #Individual scores are highest
        "diverse_teams": diverse_teams[:3],  #top 3 diverse suggestions
        "all_teams": valid_teams  #All valid teams
    }

"""

"""
def build_team(project_id: Optional[int] = None,
               team_size:int = 4,
               applicant_data:str="clean_v4", 
               score_data:str="stacking_model_scores", 
               motivation_score:str="stacking_model_moti_scores", 
               save_name:str="dream_team_example") -> dict:
"""
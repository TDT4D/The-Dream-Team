from team_building import dreamteam_builder
import json

#called from The-Dream-Team\ml>python -m scripts.team_test


#print("Begin team building")

dreamteam_builder.build_team()


"""
def build_team(project_id: Optional[int] = None,
               team_size:int = 4,
               applicant_data:str="clean_v4", 
               score_data:str="stacking_model_scores", 
               motivation_score:str="stacking_model_moti_scores", 
               save_name:str="dream_team_example") -> dict:
"""
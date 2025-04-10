from utils import storage
from typing import Optional
from collections import defaultdict
import json

"""
Data files:
clean_v4
clean_motivation_v2

meta_model_scores
stacking_model_scores

motivational_model_v1_scores
stacking_model_moti_scores

"""


def build_team(project_id: Optional[int] = None,
               team_size:int = 4,
               applicant_data:str="clean_v4", 
               score_data:str="stacking_model_scores", 
               motivation_score:str="stacking_model_moti_scores", 
               save_name:str="dream_team_example") -> dict:
    """
    Args:
        project_id (int): The project ID for which the team is being formed.
                          if None, creates teams for as many projects as possible
        team_size (int): Number of students to include in the team.
        applicant_data (str): Name of the JSON file containing cleaned version of data (example rawData cleaned using data_cleaning_version4)
        score_data (str): Name of the JSON file containing scores.
        motivation_data (str): Name of the JSON file containing motivation data.
        save_name (str): Name of the JSON file to save the created team.
   
    """
    all_teams = False

    if project_id is None:
        all_teams = True

    applicants = storage.load_json(applicant_data)
    scores = storage.load_json(score_data)
    moti_scores = storage.load_json(motivation_score)

    merged_data = merge_project_data(applicants, scores, moti_scores)

    data = add_final_scores(merged_data)


    #data = sorted(data, key=lambda x: x['final_score'], reverse=True)
    #print(json.dumps(data[:20], indent=4))

    return 


def merge_project_data(applicants, scores, moti_scores):
    """
    Merges relevant applicant data, motivation and score

    Example result:
    [
        {
            "projectId": 1052.0,
            "studentId": 20596.0,
            "whyProject": 0.042816027998924255,
            "whyExperience": 0.1357758492231369,
            "location_match": 2.0,
            "field": 4,
            "score": 87.37374114990234,
            "motivation_score": 2.5729076862335205
        }
    ]
    """
    #index scores and moti_scores by (projectId, studentId)
    score_lookup = {(s['projectId'], s['studentId']): s['Score'] for s in scores}
    moti_lookup = {(m['projectId'], m['studentId']): m['Score'] for m in moti_scores}

    #group applicants by projectId
    projects = defaultdict(list)
    for applicant in applicants:
        projects[applicant['projectId']].append(applicant)

    merged_data = []

    for project_id, applicants_list in projects.items():
        for applicant in applicants_list:
            student_id = applicant['studentId']
            key = (project_id, student_id)

            #Pull only the Score fields and rename moti score
            score = score_lookup.get(key)
            moti_score = moti_lookup.get(key)

            if score is None or moti_score is None:
                print("Score missing")
                continue #skip if either score is missing
            
            #Extract field_* with valie 1.0
            field_keys = [k for k in applicant if k.startswith('field_') and applicant[k] == 1.0]
            if len(field_keys) != 1:
                print("Error with studyfield")
                continue #Skip if no studyfield or more than one
            
            merged_data.append({
                "projectId": project_id,
                "studentId": student_id,
                "whyProject": applicant.get("whyProject"),
                "whyExperience": applicant.get("whyExperience"),
                "location_match": applicant.get("location_match"),
                "field": int(field_keys[0].split('_')[1]), #field_keys[0] OR int(field_keys[0].split('_')[1])
                "score": score,
                "motivation_score": moti_score,
            })

    return merged_data

def add_final_scores(data, f_weight=0.4, m_weight=0.3, l_weight=0.1, s_weight=0.2):
    
    #normalize weights
    total = f_weight + m_weight + l_weight + s_weight
    f_weight /= total
    m_weight /= total
    l_weight /= total
    s_weight /= total

    for row in data:
        fitting_score = row['score']
        motivation_score = row['motivation_score']
        location_score = calculate_location_score(row['location_match'])
        similarity_score = row['whyProject'] + row['whyExperience']

        similarity_score /= 2.0 #normalized to [0-1]

        final_score = (
            f_weight * fitting_score +
            m_weight * motivation_score +
            l_weight * location_score * 100 +
            s_weight * similarity_score * 100
        )

        row['final_score'] = final_score

    return data

def calculate_location_score(val):
    if val == 1.0:
        return 1.0
    elif val == 2.0: #no location data available
        return 0.5
    else:
        return 0.0

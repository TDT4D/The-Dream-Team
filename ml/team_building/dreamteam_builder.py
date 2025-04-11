from utils import storage
from typing import Optional
from collections import defaultdict
from itertools import combinations

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

    try:

        all_teams = True if project_id is None else False

        applicants = storage.load_json(applicant_data)
        scores = storage.load_json(score_data)
        moti_scores = storage.load_json(motivation_score)

        merged_data = merge_project_data(applicants, scores, moti_scores)

        data = add_final_scores(merged_data)

        #data = sorted(data, key=lambda x: x['final_score'], reverse=True)
        #print(json.dumps(data[:10], indent=4))

        """
        Example data so far:
        [
            {
                "projectId": 1047.0,
                "studentId": 22092.0,
                "whyProject": 0.7010136246681213,
                "whyExperience": 0.6258683204650879,
                "location_match": 2.0,
                "field": 17,
                "score": 94.74833679199219,
                "motivation_score": 60.20457077026367,
                "final_score": 74.22952539920807
            }
        ]

        """

        if not all_teams:
            project_applicants = [x for x in data if x['projectId'] == project_id]
            print("Project applicants: ", len(project_applicants))

            project_teams = suggest_teams_for_project(project_applicants, project_id, team_size)
            
            """
            project_teams is a list of suggested teams:
            {
            "best_overall": best_team, #average teams score highest
            "perfect_team": perfect_team, #Individual scores are highest
            "diverse_teams": diverse_teams[:3],  #top 3 diverse suggestions
            "all_teams": valid_teams  #All valid teams
            }

            """
            if project_teams is None:
                raise ValueError(f"No teams could be formed for project {project_id}.")
            
            return project_teams
        


        return 
    except Exception as e:
        print(f"Error occured, {e}")
        return None


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

def suggest_teams_for_project(project_applicants, project_id, size, top_n: Optional[int] = None):
    """
        Creates a team suggestions for an individual project
    """

    if top_n:
        applicants = sorted(project_applicants, key=lambda x: x['final_score'], reverse=True)[:top_n]
    else:
        applicants = project_applicants
    
    if len(applicants) < size:
        raise ValueError(f"Not enough applicants to form a team of size {size}. Only {len(applicants)} available.")

    team_combos = list(combinations(applicants, size))

    try:
        valid_teams = [team for team in team_combos if is_valid_team(team)]

        if not valid_teams:
            raise ValueError(f"No valid teams for project {project_id}.")

        #Team suggestions
        best_team = max(valid_teams, key=avg_score)
        perfect_team = max(valid_teams, key=lambda team: (min_individual_score(team), avg_score(team)))
        diverse_teams = sorted(valid_teams, key=lambda team: (-field_diversity(team), -avg_score(team)))

        team_suggestions = {
        "best_overall": best_team,
        "perfect_team": perfect_team,
        "diverse_teams": diverse_teams[:3],  #top 3 diverse suggestions
        "all_teams": valid_teams  #Other valid teams (includes other suggestions as well)
        }
    
        return team_suggestions
    
    except Exception as e:
        print(f"Error occured, {e}")
        return None
    
def is_valid_team(
        team, 
        score_threshold = 50, 
        unique_fields = 2, 
        only_locals = True, 
        max_score_gap = 30,
        min_team_avg = 57
):
    """
        Validates teams based on teambuilding restrictions:

        Criteria:
        - All individual scores >= score_threshold
            OR
        - Max individual score gap <= max_score_gap
        - Team has at least `unique_fields` different fields
        - If only_locals: no one with location_match == 0
        - team average >= min_team_avg
    """

    scores = [member['final_score'] for member in team]

    if not all(score >= score_threshold for score in scores):
        if max(scores) - min(scores) > max_score_gap:
            return False
    
    avg = sum(scores) / len(scores)
    if avg < min_team_avg:
        return False

    fields = {member['field'] for member in team}
    if len(fields) < unique_fields:
        #print("Too few fields")
        return False
    
    if only_locals and any(member['location_match'] == 0 for member in team):
            #print("Not local")
            return False
    
    return True

def avg_score(team):
    return sum(member['final_score'] for member in team) / len(team)

def min_individual_score(team):
    return min(member['final_score'] for member in team)

def field_diversity(team):
    return len(set(member['field'] for member in team))


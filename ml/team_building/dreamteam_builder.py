from utils import storage
from typing import Optional
from collections import defaultdict
from itertools import combinations
from utils import storage

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

        projects = sorted({entry["projectId"] for entry in data})
        print(f"Projects in dataset ({len(projects)} total)")

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

        #Suggest teams for a single project
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
            
            storage.save_json(project_teams, save_name)
            return project_teams
        
        #Suggest as many teams for all projects as possible
        suggested_teams = suggest_teams_for_all_projects(data)

        if suggested_teams is None:
                raise ValueError(f"No suggested teams something went wrong.")
            

        project_ids_with_teams = {team["projectId"] for team in suggested_teams['teams']}
        print(f"Projects with teams formed: {len(project_ids_with_teams)}")
        print(f"Project IDs: {sorted(project_ids_with_teams)}")

        """
        Suggested teams example:
        {
            "teams": final_teams,
            "project_failure_reasons": project_failure_reasons,
        }
            final_teams:
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

        storage.save_json(suggested_teams, save_name)

        return suggested_teams
    
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
        only_locals = False, 
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

def is_valid_individual(applicant, min_score=50, only_locals=False):
    if applicant['final_score'] < min_score:
        return False
    if only_locals and applicant['location_match'] == 0:
        return False
    return True

def suggest_teams_for_all_projects(
        data,
        min_score = 50,
        team_sizes = (4, 3, 5),
        only_locals = False,
        verbose = False
):
    
    used_students = set()
    final_teams = []

    # Step 1: Count project applications per student
    application_count = defaultdict(int)
    rejection_reasons = defaultdict(list)
    applicants_by_project = defaultdict(list)

    #=======================DeBugging and Justifications===========================
    # Count applicants and track rejections
    for applicant in data:
        pid = applicant['projectId']
        sid = applicant['studentId']
        applicants_by_project[pid].append(applicant)

        reason_list = []
        if applicant['final_score'] < min_score:
            reason_list.append("low score")
        if only_locals and applicant['location_match'] == 0:
            reason_list.append("non-local")
        
        if reason_list:
            rejection_reasons[pid].append((sid, reason_list))
    #=======================DeBugging and Justifications===========================

    for applicant in data:
        application_count[applicant['studentId']] += 1

    # Step 2: Group valid applicants by project
    single_project_applicants = defaultdict(list)
    multi_project_applicants = defaultdict(list)

    for applicant in data:
        sid = applicant['studentId']
        pid = applicant['projectId']
        if is_valid_individual(applicant, min_score=min_score, only_locals=only_locals):
            if application_count[sid] == 1:
                single_project_applicants[pid].append(applicant)
            else:
                multi_project_applicants[pid].append(applicant)


    # Step 2.5: Initialize project pool with all project IDs (even if empty)
    all_project_ids = {entry['projectId'] for entry in data}
    project_pool = {pid: [] for pid in all_project_ids}

    # Step 3: Assign single-project applicants first
    for pid, applicants in single_project_applicants.items():
        project_pool[pid].extend(applicants)

    # Optional debug section
    if verbose:
        print_rejection_explanations(applicants_by_project, project_pool, rejection_reasons)

    # Step 4: Add multi-project applicants to where they help most
    assigned_to_project = set()
    student_to_multi_apps = defaultdict(list)

    for pid, applicants in multi_project_applicants.items():
        for applicant in applicants:
            student_to_multi_apps[applicant['studentId']].append(applicant)


    for sid, student_apps in student_to_multi_apps.items():
        if sid in assigned_to_project or sid in used_students:
            continue

        best_score = -1
        best_pid = None
        best_applicant = None

        for applicant in student_apps:
            pid = applicant['projectId']
            pool = project_pool[pid]
            gain = diversity_gain(applicant, pool)
            ratio = diversity_ratio(pool)
            clean_div = len(pool) % 4 == 0

            penalize = clean_div and ratio > 0.25
            score = gain - (1 if penalize else 0)

            if score >= best_score:
                best_score = score
                best_pid = pid
                best_applicant = applicant

        if best_pid and best_applicant:
            project_pool[best_pid].append(best_applicant)
            assigned_to_project.add(sid)

    if verbose:
        print_applicant_pool_summary(project_pool)

    # Step 5: Build Optimal teams
    assigned_to_team = set()
    for pid, applicants in project_pool.items():
        # Remove students already used elswhere
        applicants = [a for a in applicants if a['studentId'] not in assigned_to_team]

        team_sizes_to_try = pick_team_sizes(len(applicants))

        for size in team_sizes_to_try:
            # Filter again in case the list shrank
            if len(applicants) < size:
                continue

            try:
                suggestions = suggest_teams_for_project(applicants, pid, size)
                if suggestions is None:
                    if verbose:
                        print(f"\nNo valid team found for project {pid} with size {size}")
                    raise ValueError
                team = suggestions["best_overall"]
                team_ids = {m['studentId'] for m in team}

                #Ensure uniqueness
                if not team_ids.intersection(assigned_to_team):
                    assigned_to_team.update(team_ids)
                    final_teams.append({
                    "projectId": pid,
                    "team": team,
                    "avg_score": avg_score(team),
                    "justification": generate_team_justification(team)
                    })
                
                # Remove assigned students from applicant pool
                applicants = [a for a in applicants if a['studentId'] not in team_ids]
            
            except ValueError:
                continue  # Not enough applicants or no valid team found


    project_failure_reasons = build_project_failure_reasons(
        applicants_by_project, project_pool, final_teams
    )

    if verbose:
        print_failure_summary(project_failure_reasons)

    #return final_teams

    
    return {
    "teams": final_teams,
    "project_failure_reasons": project_failure_reasons,
    }
    
def generate_team_justification(team):
    fields = {member['field'] for member in team}
    justification = []

    justification.append(
        f"Team includes students from {len(fields)} unique fields."
    )
    
    for member in team:
        reasons = []
        if member['score'] >= 85:
            reasons.append(f"is strong fit ({int(member['score'])})")
        if member['motivation_score'] >= 85:
            reasons.append(f"has high motivation ({int(member['motivation_score'])})")
        if member['location_match'] == 1.0:
            reasons.append("is local")
        if member['final_score'] >= 85:
            reasons.append(f"High overall score ({int(member['final_score'])})")
        
        member['justification'] = "Student " + ", ".join(reasons) + "."

    return justification

def avg_score(team):
    return sum(member['final_score'] for member in team) / len(team)

def min_individual_score(team):
    return min(member['final_score'] for member in team)

def field_diversity(team):
    return len(set(member['field'] for member in team))

def diversity_gain(applicant, current_applicants):
    # Adds a diversity "score" if applicant brings a new field
    fields = set(a['field'] for a in current_applicants)
    return 1 if applicant['field'] not in fields else 0

def diversity_ratio(applicants):
    field_counts = defaultdict(int)
    for a in applicants:
        field_counts[a['field']] += 1
    if not applicants:
        return 0
    return len(field_counts) / len(applicants)

def pick_team_sizes(num_applicants):
    from math import floor

    # Try all combinations of 4s and 5s first, avoid 3s unless required
    for fours in range(floor(num_applicants / 4), -1, -1):
        for fives in range((num_applicants - 4 * fours) // 5 + 1):
            remaining = num_applicants - (4 * fours + 5 * fives)
            if remaining == 0:
                return [4] * fours + [5] * fives

    # Only if a perfect 4+5 combo is not possible, introduce 3s
    for fours in range(floor(num_applicants / 4), -1, -1):
        for fives in range((num_applicants - 4 * fours) // 5 + 1):
            for threes in range((num_applicants - 4 * fours - 5 * fives) // 3 + 1):
                total = 4 * fours + 5 * fives + 3 * threes
                if total == num_applicants:
                    return [3]*threes + [4]*fours + [5]*fives

    # If nothing fits exactly, just fill with as many 4s as possible
    return [4] * (num_applicants // 4)

def print_applicant_pool_summary(project_pool):
    print("\n--- Applicant pool per project (after filtering) ---")
    for pid, pool in project_pool.items():
        print(f"Project {int(pid)}: {len(pool)} applicants")

def print_rejection_explanations(applicants_by_project, project_pool, rejection_reasons):
    print("\n==== Projects with 0 applicants or all rejected ====")
    for pid in sorted(applicants_by_project.keys()):
        total = len(applicants_by_project[pid])
        accepted = len(project_pool.get(pid, []))

        if total == 0:
            print(f"Project {int(pid)}: No students applied.")
        elif accepted == 0:
            print(f"Project {int(pid)}: All {total} applicants rejected.")
            for sid, reasons in rejection_reasons[pid]:
                print(f"  - Student {int(sid)} rejected due to: {', '.join(reasons)}")

def build_project_failure_reasons(applicants_by_project, project_pool, final_teams):
    reasons = {}
    for pid in sorted(applicants_by_project.keys()):
        all_applicants = applicants_by_project[pid]
        valid_applicants = project_pool.get(pid, [])

        if len(all_applicants) == 0:
            reasons[pid] = "No students applied."
        elif len(valid_applicants) == 0:
            reasons[pid] = f"All {len(all_applicants)} applicants were rejected (e.g., low scores, non-local)."
        elif pid not in [t['projectId'] for t in final_teams]:
            reasons[pid] = f"{len(valid_applicants)} valid applicants, but no valid team could be formed (e.g., team constraints not met)."
    return reasons

def print_failure_summary(reasons):
    print("\n==== Failed Team Formation Reasons ====")
    for pid, reason in reasons.items():
        print(f"Project {int(pid)}: {reason}")

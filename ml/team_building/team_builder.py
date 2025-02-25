from utils import storage


def build_team(n:int, project_id:int=998, load_name:str="score_test", save_name:str="team_example") -> dict:
    """
    A simple baseline for team building.
    Builds a team of top 'n' students for a given project based on their scores

    - Loads student scores from local storage
    - Filters for a specific 'projectId'
    - Sorts by 'Score' (descending order)
    - Selects the top 'n' students
    - Saves the final team to local storage
    
    Args:
        n (int): Number of students to include in the team.
        project_id (int): The project ID for which the team is being formed.
        load_name (str): Name of the JSON file containing scores.
        save_name (str): Name of the JSON file to save the created team.

    Returns:
        dict: ProjectID and the selected team of students.

    Expected input format:
    [
        {
            "projectId": 998,
            "studentId": 22058,
            "Score": 0.0
        },
        {
            "projectId": 1046,
            "studentId": 22306,
            "Score": 0.0
        }
    ]
   
    """
    data = storage.load_json(load_name)

    if not isinstance(data, list):
        print("ERROR: Invalid data format. Expected a list.")
        return None

    #Filter students for the specified `projectId`
    project_students = [student for student in data if student["projectId"] == project_id]

    if not project_students:
        print(f"WARNING: No students found for project ID {project_id}.")
        return {"projectId": project_id, "team": []}


    #Sort students by highest Score
    project_students.sort(key=lambda x: x["Score"], reverse=True)

    #Select top `n` students
    selected_team = project_students[:n]

    #Structure the response as a dictionary
    team = {"projectId": project_id, "team": selected_team}

    #Save the selected team to storage
    storage.save_json(team, save_name)

    print(f"Team of {len(selected_team)} students for project {project_id} saved as '{save_name}.json'")

    return team


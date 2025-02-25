from utils import storage


def build_team(n:int, load_name:str="student_score_example", save_name:str="team_example") -> bool:
    """
    A simple baseline for team building.
    Loads score data from local storage
    Creates a team of people with top n scores and saves it to local directory
    
    Example structure for scores
    {
        "student": 
        [
            {
                "id": 1,
                "score": 90
            },
            {
                "id": 2,
                "score": 65
            }
        ]
    }
    ___________________________________
    Expected format:
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
    ___________________________________



    Args:
        n (int): Team size
        load_name (string): file containing the scores.
        save_name (string): file containing the created team

    Returns:
        Confirmation of the team creation
    """
    data = storage.load_json(load_name)

    #Sort data to descending order
    data["student"].sort(key=lambda x: x["score"], reverse=True)

    team = {"student": data["student"][:n]}
    storage.save_json(team, save_name) #saves a copy to local storage

    return team


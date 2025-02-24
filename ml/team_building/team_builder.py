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

    team = {"stundet": data["student"][:n]}
    return storage.save_json(team, save_name)


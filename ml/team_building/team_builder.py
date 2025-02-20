import json

#Loads data as dict
#Should be replaced with database call
with open("student_score_example.json", "r") as file:
    data = json.load(file)

#print(data)
#print(data["student"][:5])

#Sort data to descending order
data["student"].sort(key=lambda x: x["score"], reverse=True)

#Create team
def build_team(n:int, data:dict) -> dict:
    """
    A simple baseline for team building.
    Creates a team of people with top n scores.
    
    Args:
        n (int): Team size
        data (dict): A sorted dict containing student scores in descending order.

    Returns:
        dict: A list of n team members.

    """
    return {"stundet": data["student"][:n]}


team = build_team(5, data)

print("Team: \n", team)

#Save team
#Should be replaced with database call
with open("team_example.json", "w") as file:
    data = json.dump(team, file)
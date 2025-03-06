from team_building import team_builder
import json

#called from The-Dream-Team\ml>python -m scripts.team_test
#should create/update 2 files containing teams
#expects student_score_example.json in local storage (data)

print("Begin team building")

"""n projectId loadName saveName"""
result = team_builder.build_team(10, project_id=1046, load_name="score_test", save_name="team_test")

filtered_result = {
    "projectId": result["projectId"],
    "team": [
        {"studentId": entry["studentId"], "Score": entry["Score"]}
        for entry in result["team"]
    ]
}

print("\nFinal team:")
print(json.dumps(filtered_result, indent=4))

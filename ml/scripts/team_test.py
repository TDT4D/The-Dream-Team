from team_building import team_builder

#called from The-Dream-Team\ml>python -m scripts.team_test
#should create/update 2 files containing teams
#expects student_score_example.json in local storage (data)

result = team_builder.build_team(5)
print("result = ", result)

result = team_builder.build_team(10, save_name="team2_example")
print("result = ", result)


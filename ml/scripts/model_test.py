from models import random_forest
import json

print("Begin model testing")
scores = random_forest.randomforest_v2(load="rawData", save_name="score_test")
print("scores done \n\n")

#Extract only relevant fields: projectId, studentId, and Score
filtered_scores = [
    {"projectId": entry["projectId"], "studentId": entry["studentId"], "Score": entry["Score"]}
    for entry in scores
]


print(json.dumps(filtered_scores, indent=4))

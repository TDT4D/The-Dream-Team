from models import get_model
import json

#called from The-Dream-Team\ml>python -m scripts.model_modular_test

print("Begin model testing")

model = get_model("randomforest_v2")

print("Begin training")

#train(data="rawData", model_name="randomforest_v2", cleaning:bool=True)
#predict(data="rawData", model_name="randomforest_v2", score_name="student_scores_default", cleaning:bool=True)
#t_predict(data="rawData", model_name="randomforest_v2_t", score_name="student_scores_t_default", cleaning:bool=True)

model.train()

print("Training completed")
print("Begin scoring")

scores = model.predict()

print("Scoring completed")

#Extract only relevant fields: projectId, studentId, and Score
filtered_scores = [
    {"projectId": entry["projectId"], "studentId": entry["studentId"], "Score": entry["Score"]}
    for entry in scores
]
print(json.dumps(filtered_scores[:10], indent=4))


print("\n Begin combined training and scoring")
t_scores = model.t_predict()

print("t_scoring completed")

#Extract only relevant fields: projectId, studentId, and Score
filtered_t_scores = [
    {"projectId": entry["projectId"], "studentId": entry["studentId"], "Score": entry["Score"]}
    for entry in t_scores
]

print(json.dumps(filtered_t_scores[:10], indent=4))

from models import get_model
import json

#can be run via \ml>python -m scripts.model_modular_test
#Models: randomforest_v2, meta_model

MODEL_NAME = "randomforest_v2"

"""
model = get_model(MODEL_NAME)

print("Begin training")

model.train("rawData", "randomforest_v2_test", True)

print("Training completed")

print("Begin scoring")
print("____________________________________________________")

scores = model.predict(data="rawData", model_name="randomforest_v2_test", score_file="randomforest_v2_test_scores", cleaning=True)

print("Scoring completed")
"""


print("Begin model testing")

model = get_model(MODEL_NAME)

print("Begin training")

#train(data="rawData", model_name="randomforest_v2", cleaning:bool=True)
#predict(data="rawData", model_name="randomforest_v2", score_file="student_scores_default", cleaning:bool=True)
#t_predict(data="rawData", model_name="randomforest_v2_t", score_file="student_scores_t_default", cleaning:bool=True)

model.train()

print("Training completed")
#_____________________________________________________
print("Begin scoring")

scores = model.predict()

print("Scoring completed")

#Extract only relevant fields: projectId, studentId, and Score
filtered_scores = [
    {"projectId": entry["projectId"], "studentId": entry["studentId"], "Score": entry["Score"]}
    for entry in scores
]
print(json.dumps(filtered_scores[:10], indent=4))

#______________________________________________________

print("\n Begin combined training and scoring")
t_scores = model.t_predict()

print("t_scoring completed")

#Extract only relevant fields: projectId, studentId, and Score
filtered_t_scores = [
    {"projectId": entry["projectId"], "studentId": entry["studentId"], "Score": entry["Score"]}
    for entry in t_scores
]

print(json.dumps(filtered_t_scores[:10], indent=4))


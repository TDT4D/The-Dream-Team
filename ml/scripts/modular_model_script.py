from models import get_model
import json

#can be run via \ml>python -m scripts.modular_model_script
#Models: randomforest_v2, meta_model

MODEL_NAME = "stacking_model"
#motivational_model_v1
#stacking_model
#meta_model

#data: clean_v4, clean_motivation_v2

model = get_model(MODEL_NAME)

print("Begin training")

model.train("clean_v4", f"{MODEL_NAME}_example", False)

print("Training completed")

print("Begin scoring")
print("____________________________________________________\n")

scores = model.predict("clean_v4", f"{MODEL_NAME}_example", f"{MODEL_NAME}_moti_scores", False)

print("Scoring completed")


#Extract only relevant fields: projectId, studentId, and Score
filtered_scores = [
    {"projectId": entry["projectId"], "studentId": entry["studentId"], "Score": entry["Score"]}
    for entry in scores
]
print(json.dumps(filtered_scores[:10], indent=4))

#use this for motivation models
"""
filtered_scores = [
    {"projectId": entry["projectId"], "studentId": entry["studentId"], "motivation": entry["motivation"]}
    for entry in scores
]
print(json.dumps(filtered_scores[:50], indent=4))
"""

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

"""

"""
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

"""
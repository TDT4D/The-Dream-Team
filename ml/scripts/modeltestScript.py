from models import get_model
from data_handling import get_cleaner
import json

#called from The-Dream-Team\ml>python -m scripts.model_test

cleaners = ["data_cleaning_version2", "data_cleaning_version3"]

models = ["randomforest_v2", "meta_model"]

#_________________________

print("initiate test for data cleaning")

print("Clean with v2")
cleaner = get_cleaner(cleaners[0])

data = cleaner.clean_data("rawData", "clean_v2")

print("Cleaning done")

print("Clean with v3")

cleaner = get_cleaner(cleaners[1])

data = cleaner.clean_data("rawData", "clean_v3")

print("Cleaning done")
#_________________________


model = get_model(models[0])

print("Begin training")

model.train("clean_v2_encoded", "randomforest_v2_1", False)

print("Training completed 1 ______________________________ \n")

model.train("clean_v3", "randomforest_v2_2", False)

print("Training completed 2 ______________________________ \n")

model = get_model(models[1])

model.train("clean_v2_encoded", "meta_model_1", False)

print("Training completed 3 ______________________________ \n")

model.train("clean_v3", "meta_model_2", False)

print("Training completed 4 ______________________________ \n")

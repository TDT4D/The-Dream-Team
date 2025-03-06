from data_handling import data_cleaning
import json

print("initiate test for data cleaning")
data = data_cleaning.clean_data_v2("rawData", "clean_test")

print("Cleaning done")
print(json.dumps(data, indent=4, ensure_ascii=False))
from data_handling import get_cleaner
import json

#ml>python -m scripts.modular_cleaning_script

cleaners = ["data_cleaning_version4", "motivation_data_cleaning_version2"]

print("initiate data cleaning")

print("Clean with v4")
cleaner = get_cleaner(cleaners[0])

data = cleaner.clean_data("rawData", "clean_v4")

print("Cleaning done")
print(json.dumps(data[:3], indent=4, ensure_ascii=False))


print("Clean with motivation v2")

cleaner = get_cleaner(cleaners[1])

data = cleaner.clean_data("rawData", "clean_motivation_v2")

print("Cleaning done")
print(json.dumps(data[:3], indent=4, ensure_ascii=False))
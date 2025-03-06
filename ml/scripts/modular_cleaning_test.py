from data_handling import get_cleaner
import json

#ml>python -m scripts.modular_cleaning_test

cleaners = ["data_cleaning_version2", "data_cleaning_version3"]

print("initiate test for data cleaning")

print("Clean with v2")
cleaner = get_cleaner(cleaners[0])

data = cleaner.clean_data("rawData", "clean_v2_modular_test")

print("Cleaning done")
print(json.dumps(data[:3], indent=4, ensure_ascii=False))


print("Clean with v3")

cleaner = get_cleaner(cleaners[1])

data = cleaner.clean_data("rawData", "clean_v3_modular_test")

print("Cleaning done")
print(json.dumps(data[:3], indent=4, ensure_ascii=False))
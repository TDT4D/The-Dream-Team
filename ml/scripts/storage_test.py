from utils import storage

#needs to be run from ml with: python -m scripts.storage_test

print(storage.load_json("test"))

print("\n")
print(storage.load_json("test.json"))

print("now try saveing \n")

data = storage.load_json("test")
print(storage.save_json("test_save", data))
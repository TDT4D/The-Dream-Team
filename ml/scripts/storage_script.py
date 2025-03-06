from utils import storage

#called from The-Dream-Team\ml>python -m scripts.storage_test
#expects test.json to be in local storage (data)

print(storage.load_json("test"))

print("\n")
print(storage.load_json("test.json"))

print("now try saveing \n")

data = storage.load_json("test")
print(storage.save_json(data, "test_save"))
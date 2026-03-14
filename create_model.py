import pickle

model = {"model": "dummy sign language model"}

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
print("model.pkl created")
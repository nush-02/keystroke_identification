import json
import pandas as pd
from features import extract_features

def build_dataset():
    with open("data/sessions.json", "r") as f:
        sessions = json.load(f)

    rows = [extract_features(s) for s in sessions]

    dataset = pd.DataFrame(rows)
    dataset.to_csv("data/keystroke_dataset.csv", index=False)
    print("[INFO] Dataset saved to data/keystroke_dataset.csv")

if __name__ == "__main__":
    build_dataset()
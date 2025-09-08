import json
import joblib
from features import extract_features
from collect import record_session

def predict_new_session():
    # Step 1: Record a new session
    user = "Unknown"   # placeholder label
    record_session(user)

    # Step 2: Load all sessions
    with open("data/sessions.json", "r") as f:
        sessions = json.load(f)

    # Step 3: Take the last session (the one we just added)
    new_session = sessions[-1]

    # Step 4: Extract features
    feats = extract_features(new_session)
    X_new = [[
        feats["dwell_avg"],
        feats["flight_avg"],
        feats["dwell_std"],
        feats["flight_std"],
        feats["accuracy"],
    ]]

    # Step 5: Remove Unknown from session

    sessions.pop()

    with open("data/sessions.json", "w") as f:
        json.dump(sessions, f, indent=4)

    # Step 5: Load trained model
    model = joblib.load("data/model.pkl")

    # Step 6: Predict
    pred = model.predict(X_new)[0]
    print(f"[RESULT] This session most likely belongs to: {pred}")

if __name__ == "__main__":
    predict_new_session()
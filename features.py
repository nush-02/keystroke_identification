import pandas as pd

def extract_features(session):
    user = session["user"]
    data = session["data"]
    accuracy = session["accuracy"]

    dwell_times = []
    flight_times = []

    last_release = None
    for entry in data:
        if entry["release"]:
            dwell = entry["release"] - entry["press"]
            dwell_times.append(dwell)

            if last_release is not None:
                flight = entry["press"] - last_release
                flight_times.append(flight)

            last_release = entry["release"]

    return {
        "user": user,
        "dwell_avg": sum(dwell_times)/len(dwell_times) if dwell_times else 0,
        "flight_avg": sum(flight_times)/len(flight_times) if flight_times else 0,
        "dwell_std": pd.Series(dwell_times).std() if dwell_times else 0,
        "flight_std": pd.Series(flight_times).std() if flight_times else 0,
        "accuracy": accuracy,
    }
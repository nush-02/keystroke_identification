import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def train_model():
    dataset_file = "data/keystroke_dataset.csv"
    model_file = "data/model.pkl"

    # Check dataset exists
    if not os.path.exists(dataset_file):
        print(f"[ERROR] Dataset not found: {dataset_file}")
        print("Run build_dataset.py first.")
        return

    # Load dataset
    df = pd.read_csv(dataset_file)

    if "user" not in df.columns:
        print("[ERROR] Dataset missing 'user' column. Did you build it correctly?")
        return

    # Features = everything except 'user'
    X = df.drop(columns=["user"])
    y = df["user"]

    # Check number of classes
    if len(set(y)) < 2:
        print("[ERROR] Need at least 2 different users to train a classifier.")
        return

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=max(0.3, len(set(y)) / len(y)), random_state=42, stratify=y
    )

    # Train RandomForest
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[INFO] Model trained. Accuracy on test set = {acc:.2f}")

    # Save
    os.makedirs("data", exist_ok=True)
    joblib.dump(model, model_file)
    print(f"[INFO] Saved model to {model_file}")

    # Show sample count per user
    counts = y.value_counts()
    print("\n[INFO] Training samples per user:")
    print(counts.to_string())

if __name__ == "__main__":
    train_model()
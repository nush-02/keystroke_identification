from pynput import keyboard
import time
import json
import os
import textdistance

session_data = []
typed_text = []

TARGET_TEXT = "the quick brown fox jumps over the lazy dog"

def on_press(key):
    try:
        char = key.char.lower() if hasattr(key, "char") and key.char else ""
        typed_text.append(char)
    except:
        pass
        
    session_data.append({"key": str(key), "press":time.time(), "release": None})

def on_release(key):
    now = time.time()
    for entry in reversed(session_data):
        if entry["release"] is None and entry["key"] == str(key):
            entry["release"] = now
            break

    if key == keyboard.Key.esc:
        return False
    
def calculate_accuracy(typed, target):
    typed_str = "".join([c for c in typed if c]).strip()
    target = target.strip()

    # Levenshtein distance
    dist = textdistance.levenshtein.distance(typed_str, target)

    # Normalize into accuracy
    accuracy = 1 - dist / max(len(target), 1)
    return accuracy

def record_session(user):
    global session_data, typed_text
    session_data = []
    typed_text = []

    print(f"[INFO] {user}, please type this sentence exactly then press ESC:")
    print(f"    >> {TARGET_TEXT}\n")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    accuracy = calculate_accuracy(typed_text, TARGET_TEXT)

    os.makedirs("data", exist_ok=True)
    file = "data/sessions.json"

    if os.path.exists(file):
        with open(file,"r") as f:
            sessions = json.load(f)
    else:
        sessions = []
        
    sessions.append({
        "user": user,
        "data": session_data,
        "typed":"".join(typed_text),
        "target": TARGET_TEXT,
        "accuracy": accuracy
    })

    with open(file, "w") as f:
        json.dump(sessions, f, indent=4)

        print(f"[INFO] Added new session for {user} with accuracy {accuracy: .2f}")

if __name__ == "__main__":
    name = input("Enter user name:")
    record_session(name)
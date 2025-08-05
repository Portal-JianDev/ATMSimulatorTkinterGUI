import json
import os
import shutil
from user import User

# Path to the main user file.
FILE_PATH = "data/users.json"

# Example file to initialize users if the main file does not exist.
EXAMPLE_FILE = "data/users_example.json"

# Loads users from the JSON file.
def load_users():
    if not os.path.exists(FILE_PATH):
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        
        if os.path.exists(EXAMPLE_FILE):
            shutil.copy(EXAMPLE_FILE, FILE_PATH)
        else:
            with open(FILE_PATH, "w") as f:
                json.dump([], f)

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [User(**u) for u in data]

# Saves the list of users to the JSON file.
def save_users(users):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        data = [u.to_dict() for u in users]
        json.dump(data, f, indent=4)

# Adds a new user if the PIN is not duplicated.
def add_user(name, pin):
    users = load_users()
    if any(u.pin == pin for u in users):
        return None

    new_user = User(name, pin, 0.0)
    users.append(new_user)
    save_users(users)
    return new_user
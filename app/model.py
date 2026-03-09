import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)  # ensure the data folder exists


def log_workout(data):
    file_path = DATA_DIR / "workouts.csv"
    df = pd.DataFrame([data])

    if file_path.exists() and file_path.stat().st_size > 0:
        # Append to existing file without header
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        # Create new file with header
        df.to_csv(file_path, index=False)


def get_workouts():
    file_path = DATA_DIR / "workouts.csv"

    if file_path.exists() and file_path.stat().st_size > 0:
        return pd.read_csv(file_path).to_dict(orient="records")

    # Return empty list if file doesn't exist or is empty
    return []


def get_macros():
    file_path = DATA_DIR / "macros.csv"

    if not file_path.exists() or file_path.stat().st_size == 0:
        # Create a CSV with default headers if missing or empty
        df = pd.DataFrame(columns=["food", "protein", "carbs", "fat", "calories"])
        df.to_csv(file_path, index=False)
        return []

    # Read and return data if file exists and is non-empty
    return pd.read_csv(file_path).to_dict(orient="records")

import pandas as pd
from pathlib import Path
import logging

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)  # ensure the data folder exists

MACROS_FILE = DATA_DIR / "macros.csv"
DEFAULT_COLUMNS = ["food", "protein", "carbs", "fat", "calories"]

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

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
    """
    Reads macros from CSV, ensures it exists, repairs bad data, and returns a list of dicts.
    """
    # Step 1: Ensure CSV exists
    if not MACROS_FILE.exists() or MACROS_FILE.stat().st_size == 0:
        logging.info("macros.csv missing or empty. Creating new file with headers.")
        df = pd.DataFrame(columns=DEFAULT_COLUMNS)
        df.to_csv(MACROS_FILE, index=False)
        return []

    try:
        # Step 2: Read CSV safely, skip bad lines
        df = pd.read_csv(MACROS_FILE, on_bad_lines="skip")

        # Step 3: Ensure all required columns exist
        for col in DEFAULT_COLUMNS:
            if col not in df.columns:
                df[col] = None

        # Keep only default columns in correct order
        df = df[DEFAULT_COLUMNS]

        # Step 4: Ensure numeric columns are numeric
        numeric_cols = ["protein", "carbs", "fat", "calories"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Step 5: Save cleaned CSV back
        df.to_csv(MACROS_FILE, index=False)

        # Step 6: Return as list of dicts
        return df.to_dict(orient="records")

    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        # Handle completely broken file
        logging.error(f"macros.csv could not be parsed: {e}. Resetting file.")
        df = pd.DataFrame(columns=DEFAULT_COLUMNS)
        df.to_csv(MACROS_FILE, index=False)
        return []

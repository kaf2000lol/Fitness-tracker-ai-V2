import pandas as pd
from pathlib import Path
import logging

# Setup
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)  # Ensure folder exists

WORKOUTS_FILE = DATA_DIR / "workouts.csv"
MACROS_FILE = DATA_DIR / "macros.csv"

WORKOUT_COLUMNS = ["date", "exercise", "sets", "reps", "weight"]  # Adjust as needed
MACRO_COLUMNS = ["food", "protein", "carbs", "fat", "calories"]

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# Workouts Functions
def log_workout(data: dict):
    """
    Logs a workout entry into workouts.csv. Creates file if missing or empty.
    
    Args:
        data (dict): Keys must match WORKOUT_COLUMNS
    """
    # Ensure file exists with headers
    if not WORKOUTS_FILE.exists() or WORKOUTS_FILE.stat().st_size == 0:
        logging.info("workouts.csv missing or empty. Creating new file with headers.")
        pd.DataFrame(columns=WORKOUT_COLUMNS).to_csv(WORKOUTS_FILE, index=False)

    df_new = pd.DataFrame([data])

    try:
        df_new.to_csv(WORKOUTS_FILE, mode="a", header=False, index=False)
        logging.info(f"Workout logged: {data}")
    except Exception as e:
        logging.error(f"Failed to log workout: {e}")


def get_workouts() -> list[dict]:
    """
    Reads workouts.csv safely, repairs missing or malformed data, and returns a list of dicts.
    
    Returns:
        List[dict]: List of workouts
    """
    if not WORKOUTS_FILE.exists() or WORKOUTS_FILE.stat().st_size == 0:
        logging.info("workouts.csv missing or empty. Creating new file with headers.")
        pd.DataFrame(columns=WORKOUT_COLUMNS).to_csv(WORKOUTS_FILE, index=False)
        return []

    try:
        df = pd.read_csv(WORKOUTS_FILE, on_bad_lines="skip")

        # Ensure all required columns exist
        for col in WORKOUT_COLUMNS:
            if col not in df.columns:
                logging.warning(f"Missing column '{col}' detected. Adding empty column.")
                df[col] = None

        df = df[WORKOUT_COLUMNS]

        # Ensure numeric columns are numeric
        for col in ["sets", "reps", "weight"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Save cleaned CSV
        df.to_csv(WORKOUTS_FILE, index=False)

        return df.to_dict(orient="records")

    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        logging.error(f"workouts.csv could not be parsed: {e}. Resetting file.")
        pd.DataFrame(columns=WORKOUT_COLUMNS).to_csv(WORKOUTS_FILE, index=False)
        return []


# Macros Functions
def get_macros():
    file_path = DATA_DIR / "macros.csv"
    columns = ["food", "protein", "carbs", "fat", "calories"]

    # create file if missing
    if not file_path.exists():
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        return []

    try:
        df = pd.read_csv(
            file_path,
            on_bad_lines="skip",   # skip corrupted rows
            engine="python"        # more tolerant parser
        )

        # ensure columns exist
        for col in columns:
            if col not in df.columns:
                df[col] = None

        df = df[columns]

        # force numeric columns
        for col in ["protein", "carbs", "fat", "calories"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # rewrite cleaned file
        df.to_csv(file_path, index=False)

        return df.to_dict(orient="records")

    except Exception:
        # if the file is completely broken, reset it
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        return []

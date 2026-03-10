import pandas as pd
from pathlib import Path
import logging
import tempfile
import os

# -----------------------------
# Setup
# -----------------------------

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

WORKOUTS_FILE = DATA_DIR / "workouts.csv"
MACROS_FILE = DATA_DIR / "macros.csv"

WORKOUT_COLUMNS = ["date", "exercise", "sets", "reps", "weight"]
MACRO_COLUMNS = ["food", "protein", "carbs", "fat", "calories"]

NUMERIC_WORKOUT_COLUMNS = ["sets", "reps", "weight"]
NUMERIC_MACRO_COLUMNS = ["protein", "carbs", "fat", "calories"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -----------------------------
# Utility Functions
# -----------------------------


def atomic_write(df: pd.DataFrame, file_path: Path):
    """
    Prevents partially written CSV files.
    Writes to temp file then renames.
    """

    with tempfile.NamedTemporaryFile(delete=False, dir=file_path.parent, suffix=".csv") as tmp:
        df.to_csv(tmp.name, index=False)
        tmp_path = Path(tmp.name)

    os.replace(tmp_path, file_path)


def create_empty_csv(file_path: Path, columns: list):
    """
    Creates a new CSV file with the correct schema.
    """

    df = pd.DataFrame(columns=columns)
    atomic_write(df, file_path)
    logging.info(f"Created new CSV file: {file_path.name}")


def safe_read_csv(file_path: Path, columns: list) -> pd.DataFrame:
    """
    Robust CSV reader that:
    - auto-detects delimiter
    - repairs missing columns
    - removes malformed rows
    - resets corrupted files
    """

    if not file_path.exists() or file_path.stat().st_size == 0:
        create_empty_csv(file_path, columns)
        return pd.DataFrame(columns=columns)

    try:

        df = pd.read_csv(
            file_path,
            sep=None,              # auto detect delimiter
            engine="python",
            on_bad_lines="skip"
        )

        # Repair missing columns
        for col in columns:
            if col not in df.columns:
                logging.warning(f"{file_path.name} missing column '{col}', repairing.")
                df[col] = None

        df = df[columns]

        return df

    except Exception as e:

        logging.error(f"{file_path.name} corrupted. Resetting file. Error: {e}")

        create_empty_csv(file_path, columns)

        return pd.DataFrame(columns=columns)


def enforce_numeric(df: pd.DataFrame, columns: list):

    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


# -----------------------------
# Workout Functions
# -----------------------------


def log_workout(data):

    exercise = str(data.get("exercise", "")).strip()
    weight = str(data.get("weight", "")).strip()
    reps = str(data.get("reps", "")).strip()
    sets = str(data.get("sets", "")).strip()

    if not exercise or not weight or not reps or not sets:
        logging.warning("Empty workout submission ignored.")
        return

    df = safe_read_csv(WORKOUTS_FILE, WORKOUT_COLUMNS)

    new_row = pd.DataFrame([{
        "exercise": exercise,
        "weight": weight,
        "reps": reps,
        "sets": sets
    }])

    df = pd.concat([df, new_row], ignore_index=True)

    atomic_write(df, WORKOUTS_FILE)

    logging.info(f"Workout logged: {data}")


def get_workouts():

    df = safe_read_csv(WORKOUTS_FILE, WORKOUT_COLUMNS)

    df = enforce_numeric(df, NUMERIC_WORKOUT_COLUMNS)

    atomic_write(df, WORKOUTS_FILE)

    return df.to_dict(orient="records")


# -----------------------------
# Macro Functions
# -----------------------------


def get_macros():

    df = safe_read_csv(MACROS_FILE, MACRO_COLUMNS)

    df = enforce_numeric(df, NUMERIC_MACRO_COLUMNS)

    atomic_write(df, MACROS_FILE)

    return df.to_dict(orient="records")

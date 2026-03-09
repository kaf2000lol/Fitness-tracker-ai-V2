import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')

def log_workout(data):
    df = pd.DataFrame([data])
    file_path = DATA_DIR / 'workouts.csv'
    if file_path.exists():
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

def get_workouts():
    file_path = DATA_DIR / 'workouts.csv'
    if file_path.exists():
        return pd.read_csv(file_path).to_dict(orient='records')
    return []

def get_macros():
    file_path = DATA_DIR / 'macros.csv'
    if file_path.exists():
        return pd.read_csv(file_path).to_dict(orient='records')
    return []

from pathlib import Path
import pandas as pd

DATA_DIR = Path('data')

def init_db():
    DATA_DIR.mkdir(exist_ok=True)
    for file_name in ['workouts.csv', 'macros.csv', 'bodyweight.csv']:
        file_path = DATA_DIR / file_name
        if not file_path.exists():
            pd.DataFrame().to_csv(file_path, index=False)

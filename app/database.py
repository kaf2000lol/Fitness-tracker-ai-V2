from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


def init_db():

    DATA_DIR.mkdir(exist_ok=True)

    for name in ["workouts.csv", "macros.csv", "bodyweight.csv"]:

        file_path = DATA_DIR / name

        if not file_path.exists():
            pd.DataFrame().to_csv(file_path, index=False)

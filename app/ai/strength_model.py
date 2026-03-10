import pandas as pd
import numpy as np
import logging
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
WORKOUTS_FILE = DATA_DIR / "workouts.csv"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class StrengthModel:
    """
    Predicts 1-rep max (1RM) for exercises using the Epley formula.
    Includes robust validation to handle corrupted or missing data.
    """

    def predict(self, workouts):

        predictions = []

        for w in workouts:

            # Safely extract fields
            exercise = str(w.get("exercise", "")).strip()

            if not exercise or exercise.lower() == "nan":
                logging.warning("Invalid exercise detected. Skipping row.")
                continue

            try:
                reps = int(float(w.get("reps", 0)))
                weight = float(w.get("weight", 0))
            except Exception:
                logging.warning(f"Invalid numeric values for {exercise}. Skipping.")
                continue

            reps = max(reps, 1)
            weight = max(weight, 0)

            predicted_1rm = weight * (1 + reps / 30)
            predicted_1rm = round(predicted_1rm)

            predictions.append({
                "exercise": exercise,
                "predicted_1rm": predicted_1rm
            })

        return predictions

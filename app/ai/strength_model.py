import pandas as pd
import numpy as np
import logging
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
WORKOUTS_FILE = DATA_DIR / "workouts.csv"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class StrengthModel:
    """
    Predicts 1-rep max (1RM) for exercises based on historical workouts.
    Uses Epley formula for estimation and can be extended to AI models.
    """

    def predict(self, workouts):
        """
        Predicts 1RM for each exercise.
        Args:
            workouts (list[dict]): List of workouts with 'exercise', 'reps', 'weight'.
        Returns:
            list[dict]: Each dict contains exercise and predicted_1rm.
        """
        predictions = []

        for w in workouts:
            exercise = w.get("exercise", "").strip()
            reps = w.get("reps", 0)
            weight = w.get("weight", 0)

            # Validate inputs
            if not exercise:
                logging.warning("Empty exercise name encountered. Skipping.")
                continue
            reps = max(int(reps), 1)
            weight = max(float(weight), 0)

            # Epley formula: 1RM = weight * (1 + reps/30)
            predicted_1rm = weight * (1 + reps / 30)

            # Round to nearest 1 lb/kg
            predicted_1rm = round(predicted_1rm)

            predictions.append({
                "exercise": exercise,
                "predicted_1rm": predicted_1rm
            })

        return predictions

import pandas as pd
import numpy as np
import logging
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
WORKOUTS_FILE = DATA_DIR / "workouts.csv"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class WeightSuggester:
    """
    Suggests weights for exercises based on historical data, exercise type, and user performance.
    Can be extended with ML models for personalized recommendations.
    """

    EXERCISE_DEFAULTS = {
        "Push-Ups": 0,
        "Squats": 20,
        "Pull-Ups": 0,
        "Lunges": 10,
        "Plank": 0,
        "Dips": 5,
        "Burpees": 0
    }

    def suggest(self, workouts):
        """
        Suggests appropriate weight for each exercise.
        Args:
            workouts (list[dict]): List of workouts with 'exercise', 'reps', 'sets', 'weight'.
        Returns:
            list[dict]: Each dict contains exercise and suggested_weight.
        """
        suggestions = []

        # Load historical data if available
        if WORKOUTS_FILE.exists() and WORKOUTS_FILE.stat().st_size > 0:
            df_history = pd.read_csv(WORKOUTS_FILE)
        else:
            df_history = pd.DataFrame(columns=["exercise", "sets", "reps", "weight", "date"])

        for w in workouts:
            exercise = w.get("exercise", "").strip()
            if not exercise:
                logging.warning("Empty exercise name encountered. Skipping.")
                continue

            # Get historical max weight for this exercise
            hist_weights = df_history[df_history["exercise"] == exercise]["weight"]
            if not hist_weights.empty:
                max_hist_weight = hist_weights.max()
            else:
                max_hist_weight = self.EXERCISE_DEFAULTS.get(exercise, 0)

            # Suggest next weight using a simple progressive overload heuristic (5-10% increment)
            suggested_weight = round(max_hist_weight * 1.05) if max_hist_weight > 0 else 5

            # Ensure non-negative weight
            suggested_weight = max(suggested_weight, 0)

            suggestions.append({
                "exercise": exercise,
                "suggested_weight": suggested_weight
            })

        return suggestions

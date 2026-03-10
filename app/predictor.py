from app.ai.strength_model import StrengthModel
from app.ai.weight_suggester import WeightSuggester

strength_model = StrengthModel()
weight_model = WeightSuggester()


def sanitize_workouts(workouts):
    """
    Cleans workout data before sending it to AI models.
    Prevents NaN / float errors from CSV parsing.
    """

    cleaned = []

    for w in workouts:

        exercise = str(w.get("exercise", "")).strip()

        if exercise.lower() == "nan" or exercise == "":
            continue

        try:
            sets = int(float(w.get("sets", 0)))
        except:
            sets = 0

        try:
            reps = int(float(w.get("reps", 0)))
        except:
            reps = 0

        try:
            weight = float(w.get("weight", 0))
        except:
            weight = 0

        cleaned.append({
            "exercise": exercise,
            "sets": sets,
            "reps": reps,
            "weight": weight
        })

    return cleaned


def predict_strength(workouts):

    workouts = sanitize_workouts(workouts)

    return strength_model.predict(workouts)


def suggest_weight(workouts):

    workouts = sanitize_workouts(workouts)

    return weight_model.suggest(workouts)

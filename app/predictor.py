from app.ai.strength_model import StrengthModel
from app.ai.weight_suggester import WeightSuggester

strength_model = StrengthModel()
weight_model = WeightSuggester()


def predict_strength(workouts):

    return strength_model.predict(workouts)


def suggest_weight(workouts):

    return weight_model.suggest(workouts)

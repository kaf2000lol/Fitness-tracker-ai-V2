from ai.strength_model import StrengthModel
from ai.weight_suggester import WeightSuggester
from model import get_workouts

strength_model = StrengthModel()
weight_model = WeightSuggester()

def predict_strength(workouts):
    return strength_model.predict(workouts)

def suggest_weight(workouts):
    return weight_model.suggest(workouts)

class StrengthModel:
    def __init__(self):
        # Load trained model here or initialize dummy
        pass

    def predict(self, workouts):
        # Return dummy predictions for now
        return [{'exercise': w.get('exercise', ''), 'predicted_1rm': 100} for w in workouts]

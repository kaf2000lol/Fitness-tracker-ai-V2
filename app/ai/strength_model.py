class StrengthModel:

    def predict(self, workouts):

        predictions = []

        for w in workouts:

            exercise = w.get("exercise", "")

            predictions.append({
                "exercise": exercise,
                "predicted_1rm": 100
            })

        return predictions

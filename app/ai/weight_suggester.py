class WeightSuggester:

    def suggest(self, workouts):

        suggestions = []

        for w in workouts:

            exercise = w.get("exercise", "")

            suggestions.append({
                "exercise": exercise,
                "suggested_weight": 50
            })

        return suggestions

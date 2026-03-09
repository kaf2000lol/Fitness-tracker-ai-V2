class WeightSuggester:
    def suggest(self, workouts):
        # Simple placeholder logic
        return [{'exercise': w.get('exercise', ''), 'suggested_weight': 50} for w in workouts]

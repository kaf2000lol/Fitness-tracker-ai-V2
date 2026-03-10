import logging
from app.ai.strength_model import StrengthModel
from app.ai.weight_suggester import WeightSuggester
from app.model import get_workouts

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def run_ai_tests():
    """
    Test harness for AI models.
    Loads workout data and runs predictions.
    """

    logging.info("Loading workout data...")
    workouts = get_workouts()

    if not workouts:
        logging.warning("No workouts found. Insert some workouts before testing.")
        return

    strength_model = StrengthModel()
    weight_model = WeightSuggester()

    logging.info("Running strength predictions...")
    strength_predictions = strength_model.predict(workouts)

    logging.info("Running weight suggestions...")
    weight_suggestions = weight_model.suggest(workouts)

    print("\n----- STRENGTH PREDICTIONS -----")

    for p in strength_predictions:
        print(f"{p['exercise']} -> Predicted 1RM: {p['predicted_1rm']}")

    print("\n----- WEIGHT SUGGESTIONS -----")

    for s in weight_suggestions:
        print(f"{s['exercise']} -> Suggested Weight: {s['suggested_weight']}")

    logging.info("AI tests completed successfully.")


if __name__ == "__main__":
    run_ai_tests()

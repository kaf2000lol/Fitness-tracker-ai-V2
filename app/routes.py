from flask import render_template, request, redirect, url_for
from app.model import log_workout, get_workouts, get_macros
from app.predictor import predict_strength, suggest_weight


def init_routes(app):

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/workout", methods=["GET", "POST"])
    def workout():

        if request.method == "POST":
            data = request.form.to_dict()
            log_workout(data)
            return redirect(url_for("progress"))

        return render_template("workout.html")

    @app.route("/progress")
    def progress():

        workouts = get_workouts()
        macros = get_macros()

        predictions = predict_strength(workouts)
        suggested_weight = suggest_weight(workouts)

        return render_template(
            "progress.html",
            workouts=workouts,
            macros=macros,
            predictions=predictions,
            suggested_weight=suggested_weight,
        )

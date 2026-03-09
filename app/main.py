from flask import Flask
from routes import init_routes
from database import init_db
from model import log_workout, get_workouts, get_macros
from predictor import predict_strength, suggest_weight

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize DB (CSV-based in this case)
init_db()

# Register routes
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)

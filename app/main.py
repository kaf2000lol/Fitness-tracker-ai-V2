from flask import Flask
from app.routes import init_routes
from app.database import init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize DB (CSV-based in this case)
init_db()

# Register routes
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)

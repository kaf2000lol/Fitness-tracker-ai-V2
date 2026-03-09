from flask import Flask
from app.routes import init_routes
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-key"

    init_db()
    init_routes(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

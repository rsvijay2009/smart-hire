from flask import Flask
from .config import Config
from .routes.main import main_bp
from .services.db_service import init_db

def create_app():
    """Initialize and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(main_bp)

    # Initialize database
    with app.app_context():
        init_db()

    return app
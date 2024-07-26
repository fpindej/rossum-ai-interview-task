from flask import Flask

from app.controllers.export.export import export_bp
from .config import Config
from .logging_setup import setup_logging


def create_app():
    setup_logging()

    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(export_bp)

    return app

from flask import Flask

from .config import Config
from .controllers.export.export import export_bp
from .logging_setup import setup_logging


def create_app():
    setup_logging(Config.LOG_LEVEL)

    app = Flask(__name__)

    # Load Config
    app.config.update(
        USERNAME=Config.USERNAME,
        PASSWORD=Config.PASSWORD
    )

    # Register Blueprints
    app.register_blueprint(export_bp)

    return app

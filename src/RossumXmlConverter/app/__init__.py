from flask import Flask
from .config import Config
from .logging_setup import setup_logging


def create_app():
    setup_logging()

    app = Flask(__name__)
    app.config.from_object(Config)

    return app

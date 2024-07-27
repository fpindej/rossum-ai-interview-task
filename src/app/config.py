import os


class Config:
    USERNAME = os.getenv('ROSSUM_USERNAME')
    PASSWORD = os.getenv('ROSSUM_PASSWORD')
    BASE_URL = 'https://pindej.rossum.app/api/v1/'
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    PORT = os.getenv('FLASK_RUN_PORT', 5000)

﻿import os


# ToDo: Separate the configurations into different classes for better organization.
class Config:
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    HOST_PORT = os.getenv('FLASK_RUN_PORT', 5000)
    # Normally these credentials would be stored in a secrets manager, this is just for demonstration purposes.
    # Also, they would probably be stored in a strongly typed object.
    USERNAME = os.getenv('ROSSUM_USERNAME')
    PASSWORD = os.getenv('ROSSUM_PASSWORD')
    # Same as above, this would be a strong type object dedicated for the Rossum API configuration.
    BASE_URL = 'https://pindej.rossum.app/api/v1/'

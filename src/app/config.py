import os

from dotenv import load_dotenv

load_dotenv()


# ToDo: Separate the configurations into different classes for better organization.
class Config:
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    HOST_PORT = os.getenv('FLASK_RUN_PORT', 5000)
    # Normally these credentials would be stored in a secrets manager, this is just for demonstration purposes.
    # Also, they would probably be stored in a strongly typed object.
    EXPORT_USERNAME = os.getenv('EXPORT_USERNAME')
    EXPORT_PASSWORD = os.getenv('EXPORT_PASSWORD')
    # Same as above, this would be a strong type object dedicated for the Rossum API configuration.
    ROSSUM_API_BASE_URL = os.getenv('ROSSUM_API_BASE_URL')
    ROSSUM_API_USERNAME = os.getenv('ROSSUM_API_USERNAME')
    ROSSUM_API_PASSWORD = os.getenv('ROSSUM_API_PASSWORD')

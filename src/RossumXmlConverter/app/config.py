import os


class Config:
    USERNAME = os.getenv('ROSSUM_USERNAME')
    PASSWORD = os.getenv('ROSSUM_PASSWORD')

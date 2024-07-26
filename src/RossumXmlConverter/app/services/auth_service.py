from app import Config


def verify_password(username, password):
    return username == Config.USERNAME and password == Config.PASSWORD

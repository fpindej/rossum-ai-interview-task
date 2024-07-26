def verify_password(username, password, stored_username, stored_password):
    return username == stored_username and password == stored_password

# A simple service to verify the username and password, which is used by the HTTPBasicAuth.verify_password decorator
# in the controller.
# I have added the verify_password function to the AuthService class, which is a simple service to verify the username
# and password that can be reimplemented with a proper authentication service in the future.
def verify_password(username, password, stored_username, stored_password):
    return username == stored_username and password == stored_password

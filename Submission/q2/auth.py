# auth.py - simple authentication, checks username/password against users.csv

import database


def authenticate(username, password):
    """checks if username and password match a user in the csv"""
    for user in database.users_data:
        if user['username'] == username and user['password'] == password:
            return {'username': user['username'], 'role': user['role']}
    return None

from course_project.firebase_config import py_firebase
from course_project.person import Person
from typing import Dict


auth = py_firebase.auth()
db = py_firebase.database()

"""This file incorporates all aspects of signing up, logging in, and logging out of the PliroMe application with 
Firebase authentication. Once the user has signed up, their information is stored to the Firebase database that can 
be accessed for future group making and purchase splitting."""


def sign_up(email: str, password: str, name: str, username: str, venmo: str) -> Dict:
    """Signs the user up and adds them to the Firebase database. If they do not input the values correctly or enter
    information such as an email or username that already exists, an error code will be returned.

    :param email: (str) The specific user's email address for their account
    :param password: (str) The specific user's password for their account
    :param name: (str) The specific user's full name (first and last name)
    :param username: (str) The specific user's username to be used when creating groups and purchases
    :param venmo: (str) The specific user's venmo username that will be accessed later for payment requests
    :return: (dictionary) containing the specific error_code (0 to pass, 1 to fail) and an associated message explaining
    what the specific issue is
    """
    users = db.child("users").get().val()
    response = {}
    if users is not None and username in users.keys():
        response['error_code'] = 1
        response['msg'] = 'Username already exists.'
        return response
    try:
        auth.create_user_with_email_and_password(email, password)
        # create the person
        Person(name, username, email, venmo)
        response['error_code'] = 0
        response['msg'] = "Account successfully created! Log in now."
    except Exception as e:
        # TODO: Make error output correct
        response['error_code'] = 1
        response['msg'] = "Email already exists, please use a new email address to log in!"

    return response


def login(email: str, password: str) -> Dict:
    """Logs the user into the PliroMe system, giving them access to access their profile, group memberships, and purchases.

    :param email: (str) The specific email that you used to sign up with PliroMe
    :param password: (str) The specific password that you used to keep your account secure
    :return: (dictionary) that includes an error code (0 if passed, 1 if failed) and a message associated with the
    specific error code"""
    response = {}
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        auth.refresh(user['refreshToken'])
        all_users = db.child("users").order_by_child('email').equal_to(email).get()

        # check to see the user is there
        for user in all_users.each():
            # there should only be one match
            username = user.key()
            user.val()
            response['username'] = username

        response['error_code'] = 0
        response['msg'] = "Successfully logged in with email: " + email + "!"
        response['user_id'] = auth.current_user
    except Exception as e:
        response['error_code'] = 1
        response['msg'] = "Invalid email or password. Please try again."

    return response


def logout():
    """Logs the current user out of the PliroMe system. Their information is still stored in the Firebase database so
    that the user can log back in and access their information later"""
    auth.current_user = None

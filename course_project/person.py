from course_project.firebase_config import py_firebase
from venmo_api import Client

db = py_firebase.database()
auth = py_firebase.auth()
storage = py_firebase.storage()


# The py_firebase database adds each new individual user

# Person Class with Name, Username, Email, Venmo, and a list of groups the user is currently involved in

class Person:
    """This class holds all of the information about each individual user of PliroMe. When the person is initialized,
    their email, group memberships, name, username, and venmo are all stored under their specific username as the heading.
    Once a person's information is stored, they can log in and access their information for later use when creating
    groups and adding purchases"""

    def __init__(self, name: str, username: str, email: str, venmo: str):
        """Initializes a user in the Firebase database, storing all of their information such as their name, username,
        email, venmo, and a list of groups that the user is a part of

        :param name: (str) The full name of the user being added to the database
        :param username: (str) The unique username that will be associated with this specific account
        :param email: (str) The unique email that will be associated with this specific account
        :param venmo: (str) The Venmo account that will be associated with this specific account"""
        if name == "" or username == "" or email == "" or venmo == "":
            return
        self.name = name
        self.username = username
        self.email = email
        self.venmo = venmo
        self.groups = []
        db.child("users").child(username).set(" ")
        db.child("users").child(username).child("name").set(name)
        db.child("users").child(username).child("groups").set("")
        db.child("users").child(username).child("venmo").set(venmo)
        db.child("users").child(username).child("username").set(username)
        db.child("users").child(username).child("email").set(email)
        db.child("users").child(username).child("has_profile_picture").set("False")


def remove_email_from_auth(email: str, password: str):
    """ Deletes an email from the authentication database

    ::param email: (str) The email you would like to delete
    ::param password: (str) The password associated with this email
    """
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        auth.delete_user_account(user['idToken'])
    except:
        # do nothing, email does not exist
        pass


def get_user_balance(username: str):
    """Gets the specific user's balance

    :param username: (str) The unique username that will be used to find the balance
    :return: (float) The balance that the user has, negative if they owe money and positive if they need to be paid
    """

    return db.child("users").child(username).child("balance").get().val()


def get_access_token(username: str, venmo_email: str, venmo_password: str):
    """Gets the user's access token from the Venmo api

    :param username: (str) The user's unique username
    :param venmo_email: (str) The email associated with the user's Venmo account, entered by the user
    :param venmo_password: (str) The password associated with the user's Venmo account, entered by the user
    """

    access_token = input(Client.get_access_token(username=venmo_email, password=venmo_password))
    db.child("users").child(username).child("access_token").set(access_token)


def add_profile_picture(profile_picture_path: str, username: str):
    """Adds a receipt to the specific group for a purchase that is made

    :param profile_picture_path: (str) Location of the image that you would like to upload
    :param username: (str) The name of the person you would like to upload the image to
    """
    picture_name = username + '_profile_picture' + '.JPG'
    storage.child(picture_name).put(profile_picture_path)
    db.child("users").child(username).child("has_profile_picture").set("True")


def get_profile_picture(username: str) -> str:
    """Returns a list of all the receipts that are present within a group

    :param username: (str) The name of the specific person that you would like to get the profile picture of
    :return: (str) The link to the profile picture from the storage
    """

    picture_name = username + '_profile_picture' + '.JPG'
    pic_link = storage.child(picture_name).get_url(None)

    return pic_link


def get_default_profile_picture() -> str:
    """Returns the link to the storage for the default profile picture.

    :return: (str) The link to the default profile picture"""
    picture_name = 'default_profile_picture.jpg'
    pic_link = storage.child(picture_name).get_url(None)
    return pic_link


def has_profile_picture(username: str) -> bool:
    """ Returns whether or not person has a profile picture.

    :param username: (str) The name of the specific person that you would like to get the profile picture of
    :return: (bool) True or False of whether or not the person has a profile picture
    """
    has_picture = db.child("users").child(username).child("has_profile_picture").get().val()
    if has_picture is None:
        db.child("users").child(username).child("has_profile_picture").set("False")
        has_picture = "False"
    if has_picture == "True":
        return True
    else:
        return False


def delete_user(username: str):
    """Deletes the user from the database"""
    db.child("users").child(username).remove()

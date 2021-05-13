import json

from course_project.person import Person
from course_project.purchase import Purchase
from course_project.firebase_config import py_firebase
from venmo_api import Client

db = py_firebase.database()
storage = py_firebase.storage()


class Group:
    """This class includes the functionality behind creating a group within our application, adding members, and
    splitting purchases. Additionally, this file also includes functions that assist with accessing a list of all the
    users in our data, all of the groups for a specific user, all of the users for a specific group, all of the
    purchases included within a group, and finally deleting a group."""

    def __init__(self, name: str, group=[], time_cycle=14):
        """ Initializes a Group with a name, list of usernames, and a time cycle; Adds them to the Firebase database

        :param name: (str) The unique identifier that will be used in order to distinguish the group from others
        :param group: (array) An empty array that the group member's usernames will be appended to
        :param time_cycle=14: (int) The number of days in between each purchase.
        """
        if name == "":
            return
        self.group = group  # this represents the members in the group by their username
        self.number_of_members = 0
        self.purchases = []  # a list where the key is a person's username and the value is an object of type
        self.name = name  # this will be a unique identifier. Verify uniqueness by the frontend.
        self.time_cycle = time_cycle  # days between payment requests are sent out. 14 days is default
        self.group_usernames = []
        for person in group:
            self.group_usernames.append(person.name)

        db.child("groups").child(name).set(" ")
        db.child("groups").child(name).child("name").set(name)
        db.child("groups").child(name).child("members").set(self.group_usernames)
        db.child("groups").child(name).child("time_cycle").set(time_cycle)
        db.child("groups").child(name).child("purchases").set("")
        db.child("groups").child(name).child("receipt_count").set(0)
        db.child("groups").child(name).child("has_group_picture").set("False")

    def add_member(self, username: str):
        """Add a new user to the group by their username. This function also adds the member to the group inside the
        Firebase database, and updates the individual users in real time to update their group memberships as well.

        :param username: (str) The name of the specific user you would like to add to your group.
        """

        # get all the users in the group
        all_users = get_all_users()
        if username not in all_users:
            return Exception('username is not in the current database.')

        # add a member to the group in the database
        self.group_usernames.append(username)
        self.number_of_members += 1
        db.child("groups").child(self.name).child("members").set(self.group_usernames)
        curr_groups = list(db.child('users').child(username).child('groups').get().val())
        # add a group to the member in the database
        if curr_groups is None:
            curr_groups = []
        elif type(curr_groups) is str:
            curr_groups = [curr_groups]
        curr_groups.append(self.name)
        db.child('users').child(username).child('groups').set(curr_groups)


def split_purchases(group_name: str, send_venmos: bool = False):
    """ start by making a graph that shows how much is owed between everyone.
    The top row will have everyone's name and the first column has everyone's name.

    Splits the purchases amongst the user within a specific group.

    :param group_name: (str) The name of the group whose purchases need to be split
    :param send_venmos: (bool) A bool indicating whether or not Venmo requests should be sent

    :return: (array) containing tuples of (the person who ... )"""
    group_usernames = db.child("groups").child(group_name).child("members").get().val()
    graph = {}
    for person0 in group_usernames:
        graph[person0] = {}
        for person1 in group_usernames:
            graph[person0][person1] = 0

    purchases = db.child("groups").child(group_name).child("purchases").get().val()

    # Creates a graph for the recipients and buyers with the amount of money that is owed.
    for purchase in purchases:
        for recipient in purchases[purchase]["recipients"]:
            graph[purchases[purchase]["buyer"]][recipient] += float(purchases[purchase]["recipients"][recipient])
    # print(graph)

    # Creates a list of tuples from the above graph
    venmos = []
    for p0 in range(0, len(group_usernames)):
        for p1 in range(p0 + 1, len(group_usernames)):
            person0 = group_usernames[p0]
            person1 = group_usernames[p1]
            owed = graph[person0][person1] - graph[person1][person0]
            if owed < 0:
                owedNegative = owed * -1
                venmos.append((person1, person0, owedNegative))
            elif owed > 0:
                venmos.append((person0, person1, owed))

    if (send_venmos):
        for request in venmos:
            personOwed = request[0]
            personOwing = request[1]
            owed = request[2]
            try:
                personOwedAccessToken = db.child("users").child(personOwed).child("access_token").get().val()
                print(personOwedAccessToken)
            except:
                print("Failed to get access token")
                continue
            venmo = Client(personOwedAccessToken)
            print(venmo.user.get_my_profile())
            try:
                # mprint(personOwing)
                personOwingVenmo = db.child("users").child(personOwing).child("venmo").get().val()
                # print(personOwingVenmo)
                personOwingID = venmo.user.search_for_users(query=personOwingVenmo)[0].id
                print(personOwingID)
                print("HERE")
                venmo.payment.request_money(int(owed), "PliroMe Request", personOwingID)
            except:
                print("Error with Venmo request")

    return venmos


# Return a list of all the users
def get_all_users():
    """ Returns a list of all the users in the database

    :return: (list) of all the individuals located in the "users" section of the Firebase database system
    """
    return list(db.child("users").shallow().get().val())


# Return all groups of a specific user
def get_all_user_groups(username: str) -> list:
    """ Returns all groups of a specific user

    :param username: (str) The name of the specific user you would like to access
    :return: (list) of all of groups that a user is a member of
    """
    if len(list(db.child("users").child(username).child('groups').get().val())) == 0 or \
            list(db.child("users").child(username).child('groups').get().val()) is None:
        return []
    else:
        return list(db.child("users").child(username).child('groups').get().val())


# Return all users within a specific group
def get_all_users_in_group(group_name: str) -> list:
    """ Returns all users within a specific group

    :param group_name: (str) The name of the specific group you would like to access
    :return: (list) of all the individual members within a group
    """
    return list(db.child("groups").child(group_name).child("members").get().val())


# Return all venmo usernames of users in a group
def get_all_venmos_in_group(group_name: str) -> []:
    """ Returns all venmos within a specific group

    :param group_name: (str) The name of the specific group you would like to access
    :return: (list) of all the individual venmo usernames within a group
    """
    members = list(db.child("groups").child(group_name).child("members").get().val())
    venmos = []

    for person in members:
        venmos.append(db.child("users").child(person).child("venmo").get().val())

    return venmos


# Return all purchases inside of a group
def get_all_purchases_for_group(group_name: str) -> ([], [], []):
    """Return all of the purchases inside of a specific group

    :param group_name: (str) The specific group you want to access the purchases for
    :return: (array) "items" of all of the names of the purchases
    :return: (array) "buyers" of all of the names of the members that bought these specific purchases
    :return: (array) "prices" of all of the values that the purchases cost
    """
    purchases = db.child("groups").child(group_name).child("purchases").get()
    items = []
    buyers = []
    prices = []
    if purchases.each() is not None:
        for purchase in purchases.each():
            items.append(purchase.key())
            buyers.append(purchase.val()['buyer'])
            prices.append(purchase.val()['price'])
    return items, buyers, prices


# Delete a group by removing it from the database and clearing that group from all users
def delete_group(group_name: str):
    """Deletes a group by removing it from the database and clearing that group from all users

    :param group_name: (str) The name of the specific group you would like to delete
    """

    try:
        delete_all_purchases(group_name)
        all_group_users = get_all_users_in_group(group_name)
        db.child("groups").child(group_name).remove()

        for username in all_group_users:
            curr_groups = list(db.child('users').child(username).child('groups').get().val())
            curr_groups.remove(group_name)
            db.child('users').child(username).child('groups').set(curr_groups)
    except:
        # group does not exist, do nothing
        return Exception("Something went wrong!")


# Allows deletion of a purchase
def delete_purchase(group_name: str, purchase_name: str):
    """Deletes a purchase by removing it from the database and resetting balances of people involved

    :param group_name: (str) The name of the specific group you would like to delete
    :param purchase_name: (str) The name of the purchase to be deleted
    """
    purchases = db.child("groups").child(group_name).child("purchases").get().val()
    if purchase_name in purchases.keys():
        price = float(db.child("groups").child(group_name).child("purchases").
                      child(purchase_name).child("price").get().val())
        recips = db.child("groups").child(group_name).child("purchases"). \
            child(purchase_name).child("recipients").get().val()
        buyer = db.child("groups").child(group_name).child("purchases"). \
            child(purchase_name).child("buyer").get().val()
        print(buyer)
        buyers_bal = float(db.child("users").child(buyer).child("balance").get().val())
        for recipient in recips:
            if recipient != buyer:
                bal = float(db.child("users").child(recipient).child("balance").get().val())
                amount_paid = float(db.child("groups").child(group_name).child("purchases").
                                    child(purchase_name).child("recipients").child(recipient).get().val())
                bal += amount_paid
                buyers_bal -= amount_paid
                print(buyers_bal)
                db.child("users").child(recipient).child("balance").set(bal)
        db.child("users").child(buyer).child("balance").set(buyers_bal)
        db.child("groups").child(group_name).child("purchases").child(purchase_name).remove()

    return


# Deletes all purchases from group
def delete_all_purchases(group_name: str):
    """Runs delete purchase on every purchase in group

    :param group_name: (str) The name of the specific group you would like to delete
    """
    purchases = db.child("groups").child(group_name).child("purchases").get().val().keys()
    for purchase in purchases:
        delete_purchase(group_name, purchase)


# Allows the user to leave a group from the database
def leave_group(group_name: str, username: str):
    """Allows the user to leave a group that they are currently in

    :param group_name: (str) The name of the group that the user would like to leave
    :param username: (str) The name of the user that you would like to use to leave that specific group
    """
    try:
        group_users = get_all_users_in_group(group_name)
        group_users.remove(username)
        db.child("groups").child(group_name).child("members").set(group_users)
        user_groups = get_all_user_groups(username)
        print(user_groups)
        user_groups.remove(group_name)
        if not user_groups:
            db.child("users").child(username).child("groups").set("")
        else:
            db.child("users").child(username).child("groups").set(user_groups)
    except:
        # username or group does not exist, do nothing
        pass


def add_receipt(receipt_path: str, group_name: str):
    """Adds a receipt to the specific group for a purchase that is made

    :param receipt_path: (str) Location of the image that you would like to upload
    :param group_name: (str) The name of the group you would like to upload the image to
    """
    num = db.child('groups').child(group_name).child('receipt_count').get().val()
    receipt_name = group_name + str(num) + ".JPG"
    storage.child(receipt_name).put(receipt_path)
    db.child("groups").child(group_name).child("receipt_count").set(num + 1)


def get_recipts(group_name: str) -> []:
    """Returns a list of all the receipts that are present within a group

    :param group_name: (str) The name of the specific group that you would like to access"""
    receipt_links = []
    num = db.child('groups').child(group_name).child('receipt_count').get().val()
    for i in range(num):
        receipt_name = group_name + str(i) + ".JPG"
        receipt_link = storage.child(receipt_name).get_url(None)
        receipt_links.append(receipt_link)

    return receipt_links


def add_group_picture(group_picture_path: str, group_name: str):
    """Adds a receipt to the specific group for a purchase that is made

    :param group_picture_path: (str) Location of the image that you would like to upload
    :param group_name: (str) The name of the group you would like to upload the image to
    """
    picture_name = group_name + '_group_picture' + '.JPG'
    storage.child(picture_name).put(group_picture_path)
    db.child("groups").child(group_name).child("has_group_picture").set("True")


def get_group_picture(group_name: str) -> str:
    """Returns a list of all the receipts that are present within a group

    :param group_name: (str) The name of the specific group that you would like to get the group picture of
    :return: (str) The link to the group picture from the storage
    """

    picture_name = group_name + '_group_picture' + '.JPG'
    pic_link = storage.child(picture_name).get_url(None)

    return pic_link


def get_default_group_picture() -> str:
    """Returns the link to the storage for the default group picture.

    :return: (str) The link to the default profile picture"""
    picture_name = 'default_group_picture.jpg'
    pic_link = storage.child(picture_name).get_url(None)
    return pic_link


def has_group_picture(group_name: str) -> bool:
    """ Returns whether or not a group has a picture.

    :param group_name: (str) The name of the specific group that you would like to get the group picture of
    :return: (bool) True or False of whether or not the group has a group picture
    """
    has_picture = db.child("groups").child(group_name).child("has_group_picture").get().val()
    if has_picture is None:
        db.child("groups").child(username).child("has_group_picture").set("False")
        has_picture = "False"
    if has_picture == "True":
        return True
    else:
        return False

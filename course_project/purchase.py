from course_project.person import Person
from course_project.firebase_config import py_firebase

db = py_firebase.database()


class Purchase:
    """The purchase class stores data for each purchase that gets entered into a group. It can hold a picture (receipt),
    the price, and later will contain info about which group members owe money for it.
    The percentage that each recipient owes is stored next to their name in the recipients file."""

    def __init__(self, buyer: str, group: str, item: str, price: int, recipients={}):
        """Initializes a purchase and adds it to the database for a specific group. The heading will be the type of item
        that they purchased, and when you see the information in Firebase it contains information on the buyer, as well
        as the price of the item

        :param buyer: (str) The username of the specific buyer of the purchase
        :param group: (str) The name of the specific group that the purchase will be added to
        :param item: (str) The name of the specific item that was purchased
        :param price: (int) The price of the item that was bought"""

        self.buyer = buyer
        self.group = group
        self.item = item
        self.price = price

        if buyer == "" or group == "" or item == "" or price == "":
            return

        db.child("groups").child(group).child("purchases").child(item).set("")
        db.child("groups").child(group).child("purchases").child(item).child("buyer").set(buyer)
        db.child("groups").child(group).child("purchases").child(item).child("price").set(price)

        db.child("groups").child(group).child("purchases").child(item).child("recipients").set("")
        for recipient in recipients.keys():
            set_price = float(price) * float(recipients[recipient]) / 100
            db.child("groups").child(group).child("purchases").child(item).child("recipients"). \
                child(recipient).set(set_price)

        for person in recipients.keys():
            if person != buyer:
                try:
                    balance = int(db.child("users").child(person).child("balance").get().val())
                    # print("balance = " + str(balance))
                except:
                    balance = 0
                balance -= float(price) * float(recipients[person]) / 100
                db.child("users").child(person).child("balance").set(balance)
        try:
            balance = int(db.child("users").child(buyer).child("balance").get().val())
            # print("balance = " + balance)
        except:
            balance = 0
        print(recipients)
        balance += float(price) - (float(price) * float(recipients[buyer]) / 100)
        db.child("users").child(buyer).child("balance").set(balance)

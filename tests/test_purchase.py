import unittest
from course_project import purchase
from course_project import group
from course_project.firebase_config import py_firebase

db = py_firebase.database()


class Purchase(unittest.TestCase):
    def test_add_purchase(self):
        db.child("groups").child("test_add_purchase").remove()
        group.Group("test_add_purchase")
        original_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_original_purchases = len(original_purchases)
        purchase.Purchase('adit', 'test_add_purchase', 'coffee', 1345, {'adit': 100})
        new_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_new_purchases = len(new_purchases)
        self.assertEqual(len_original_purchases + 1, len_new_purchases)

    def test_add_purchase_no_buyer(self):
        db.child("groups").child("test_add_purchase").remove()
        group.Group("test_add_purchase")
        original_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_original_purchases = len(original_purchases)
        purchase.Purchase('', 'test_add_purchase', 'coffee', 1345, {'adit': 100})
        new_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_new_purchases = len(new_purchases)
        self.assertEqual(len_original_purchases, len_new_purchases)

    def test_add_purchase_no_group(self):
        db.child("groups").child("test_add_purchase").remove()
        group.Group("test_add_purchase")
        original_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_original_purchases = len(original_purchases)
        purchase.Purchase('testing', '', 'coffee', 1345, {'adit': 100})
        new_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_new_purchases = len(new_purchases)
        self.assertEqual(len_original_purchases, len_new_purchases)

    def test_add_purchase_no_name(self):
        db.child("groups").child("test_add_purchase").remove()
        group.Group("test_add_purchase")
        original_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_original_purchases = len(original_purchases)
        purchase.Purchase('testing', 'test_add_purchase', '', 1345, {'adit': 100})
        new_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_new_purchases = len(new_purchases)
        self.assertEqual(len_original_purchases, len_new_purchases)

    def test_add_purchase_no_price(self):
        db.child("groups").child("test_add_purchase").remove()
        group.Group("test_add_purchase")
        original_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_original_purchases = len(original_purchases)
        purchase.Purchase('testing', 'test_add_purchase', 'coffee', '', {'adit': 100})
        new_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_new_purchases = len(new_purchases)
        self.assertEqual(len_original_purchases, len_new_purchases)

    def test_add_percentages(self):
        db.child("groups").child("test_add_purchase").remove()
        group.Group("test_add_purchase")
        original_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_original_purchases = len(original_purchases)
        purchase.Purchase('adit', 'test_add_purchase', 'coffee', 1345, {'adit': 33, 'Morty1': 33, 'Morty2': 34})
        new_purchases = db.child("groups").child('test_add_purchase').child("purchases").get().val()
        len_new_purchases = len(new_purchases)
        self.assertEqual(len_original_purchases + 1, len_new_purchases)

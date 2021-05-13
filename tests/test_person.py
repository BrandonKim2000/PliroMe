import unittest
from course_project.person import Person
from course_project import person
from course_project.firebase_config import py_firebase

db = py_firebase.database()


class PersonTests(unittest.TestCase):
    def test_add_person(self):
        db.child("users").child("Morty").remove()
        all_users = db.child("users").get().val()
        prev_users_count = len(all_users)
        Person("Morty", "Morty", "Morty@gmail.com", "Morty_venmo")
        all_users = db.child("users").get().val()
        updated_users_count = len(all_users)
        self.assertEqual(prev_users_count+1, updated_users_count)
        db.child("users").child("Morty").remove()

    def test_add_person_no_name(self):
        db.child("users").child("Morty").remove()
        all_users = db.child("users").get().val()
        prev_users_count = len(all_users)
        Person("", "Morty", "Morty@gmail.com", "Morty_venmo")
        all_users = db.child("users").get().val()
        updated_users_count = len(all_users)
        self.assertEqual(prev_users_count, updated_users_count)

    def test_add_person_no_username(self):
        db.child("users").child("Morty").remove()
        all_users = db.child("users").get().val()
        prev_users_count = len(all_users)
        Person("Morty", "", "Morty@gmail.com", "Morty_venmo")
        all_users = db.child("users").get().val()
        updated_users_count = len(all_users)
        self.assertEqual(prev_users_count, updated_users_count)
        db.child("users").child("Morty").remove()

    def test_add_person_no_email(self):
        db.child("users").child("Morty").remove()
        all_users = db.child("users").get().val()
        prev_users_count = len(all_users)
        Person("Morty", "Morty", "", "Morty_venmo")
        all_users = db.child("users").get().val()
        updated_users_count = len(all_users)
        self.assertEqual(prev_users_count, updated_users_count)
        db.child("users").child("Morty").remove()

    def test_add_person_no_venmo(self):
        db.child("users").child("Morty").remove()
        all_users = db.child("users").get().val()
        prev_users_count = len(all_users)
        Person("Morty", "Morty", "Morty@gmail.com", "")
        all_users = db.child("users").get().val()
        updated_users_count = len(all_users)
        self.assertEqual(prev_users_count, updated_users_count)
        db.child("users").child("Morty").remove()

    def test_add_person_profile_picture(self):
        db.child("users").child("Morty").remove()
        Person("Morty", "Morty", "Morty@gmail.com", "morty-venmo")
        person.add_profile_picture(None, "Morty")
        self.assertTrue(person.has_profile_picture("Morty"))

    def test_no_person_profile_picture(self):
        db.child("users").child("Morty").remove()
        Person("Morty", "Morty", "Morty@gmail.com", "morty-venmo")
        self.assertFalse(person.has_profile_picture("Morty"))

    def test_get_default_profile_picture(self):
        db.child("users").child("Morty").remove()
        Person("Morty", "Morty", "Morty@gmail.com", "morty-venmo")
        pic_link = person.get_default_profile_picture()
        self.assertFalse(pic_link is None)

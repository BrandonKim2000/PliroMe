import unittest
from course_project.person import Person
from course_project import group
from course_project.group import Group
from course_project.purchase import Purchase
from course_project.firebase_config import py_firebase

db = py_firebase.database()


# coverage run --source=pyarcade -m unittest discover > stdout.out


class TestGroups(unittest.TestCase):
    def test_add_group(self):
        db.child("groups").child("test_add_group").remove()
        all_groups = db.child("groups").get().val()
        prev_group_count = len(all_groups)
        Group("test_add_group")
        new_groups = db.child("groups").get().val()
        updated_group_count = len(new_groups)
        self.assertEqual(prev_group_count + 1, updated_group_count)
        db.child("groups").child("test_add_group").remove()

    def test_add_group_no_name(self):
        db.child("groups").child("test_add_group").remove()
        all_groups = db.child("groups").get().val()
        prev_group_count = len(all_groups)
        Group("")
        new_groups = db.child("groups").get().val()
        updated_group_count = len(new_groups)
        self.assertEqual(prev_group_count, updated_group_count)

    def test_group_add_member(self):
        db.child("users").child("Morty").remove()
        Person("Morty", "Morty", "Morty@gmail.com", "Morty_venmo")
        Person("Morty2", "Morty2", "Morty2@gmail.com", "Morty2_venmo")
        print("HERE")

        db.child("groups").child("test_add_member").remove()
        curr_group = Group("test_add_member")
        curr_group.add_member("Morty")
        curr_group.add_member("Morty2")
        members = db.child("groups").child("test_add_member").child("members").get().val()
        self.assertEqual(len(members), 2)

    def test_get_venmos(self):
        p0 = Person("b0", "b0", "b0", "b0")
        p1 = Person("b1", "b1", "b1", "b1")
        p2 = Person("b2", "b2", "b2", "b2")
        p3 = Person("b3", "b3", "b3", "b3")
        group = Group("test group", [p0, p1, p2, p3])

        Purchase("b0", "test group", "sausage", 400, {"b0": 25, "b1": 25, "b2": 25, "b3": 25})

    def test_get_venmos2(self):
        p0 = Person("b0", "b0", "b0", "b0")
        p1 = Person("b1", "b1", "b1", "b1")
        p2 = Person("b2", "b2", "b2", "b2")
        p3 = Person("b3", "b3", "b3", "b3")
        group = Group("test group", [p0, p1, p2, p3])

        # Purchase("b0", "test group", "sausage", 400, {"b0": 25, "b1": 25, "b2": 25, "b3": 25})
        print("WORKED")

    def test_split(self):
        p0 = Person("b0", "b0", "b0", "b0")
        p1 = Person("b1", "b1", "b1", "b1")
        p2 = Person("b2", "b2", "b2", "b2")
        p3 = Person("b3", "b3", "b3", "b3")
        gr = Group("Test Split Purchases", [p0, p1, p2, p3])
        Purchase("b0", "Test Split Purchases", "sausage", 400, {"b0": 25, "b1": 25, "b2": 25, "b3": 25})
        ret = group.split_purchases("Test Split Purchases")
        self.assertEqual(int(ret[0][2]), int(100))

    def test_leave_group(self):
        p0 = Person("t0", "t0", "t0", "t0")
        p1 = Person("t1", "t1", "t1", "t1")
        p2 = Person("t2", "t2", "t2", "t2")
        p3 = Person("t3", "t3", "t3", "t3")
        Group("leave group", [p0, p1, p2, p3])
        group.leave_group("leave group", "t1")
        self.assertEqual(3, len(group.get_all_users_in_group("leave group")))
        group.delete_group("leave group")

    def test_leave_group_invalid_group_name(self):
        p0 = Person("t0", "t0", "t0", "t0")
        p1 = Person("t1", "t1", "t1", "t1")
        p2 = Person("t2", "t2", "t2", "t2")
        p3 = Person("t3", "t3", "t3", "t3")
        Group("leave group", [p0, p1, p2, p3])
        group.leave_group("leav group", "t1")
        self.assertRaises(Exception)
        group.delete_group("leave group")

    def test_leave_group_invalid_username(self):
        p0 = Person("t0", "t0", "t0", "t0")
        p1 = Person("t1", "t1", "t1", "t1")
        p2 = Person("t2", "t2", "t2", "t2")
        p3 = Person("t3", "t3", "t3", "t3")
        Group("leave group", [p0, p1, p2, p3])
        group.leave_group("leave group", "t4")
        self.assertRaises(Exception)
        group.delete_group("leave group")

    def test_add_group_picture(self):
        db.child("groups").child("test_group_pic").remove()
        Group("test_group_pic")
        group.add_group_picture(None, "test_group_pic")
        self.assertTrue(group.has_group_picture("test_group_pic"))

    def test_no_group_picture(self):
        db.child("groups").child("test_group_pic").remove()
        Group("test_group_pic")
        self.assertFalse(group.has_group_picture("test_group_pic"))

    def test_get_default_profile_picture(self):
        db.child("groups").child("test_group_pic").remove()
        Group("test_group_pic")
        pic_link = group.get_default_group_picture()
        self.assertFalse(pic_link is None)

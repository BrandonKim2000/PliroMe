import unittest
import io
from course_project.app import create_app
from course_project import group
from course_project import person
from course_project.person import Person


class ApplicationLoginTestCase(unittest.TestCase):
    def test_can_access_home_page(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_successful(self):
        flask_app = create_app()
        client = flask_app.test_client()
        person.delete_user("testcanlogin")
        person.remove_email_from_auth("testcanlogin@gmail.com", "password")

        response = client.post('/signup', data=dict(email="testcanlogin@gmail.com",
                                                    password="password",
                                                    username="testcanlogin",
                                                    name="testcanlogin",
                                                    venmo="testcanlogin"),
                               follow_redirects=True)

        response = client.post('/login', data=dict(email="testcanlogin@gmail.com", password="password"),
                               follow_redirects=True)
        self.assertIn(b'test', response.data)
        self.assertIn(b'Click "+" to create a group!', response.data)

        person.delete_user("testcanlogin")
        person.remove_email_from_auth("testcanlogin@gmail.com", "password")

    def test_login_with_incorrect_password(self):
        flask_app = create_app()
        client = flask_app.test_client()
        person.delete_user("testloginincorrectpassword")
        person.remove_email_from_auth("testloginincorrectpassword@gmail.com", "password")

        response = client.post('/signup', data=dict(email="testloginincorrectpassword@gmail.com",
                                                    password="password",
                                                    username="testloginincorrectpassword",
                                                    name="testloginincorrectpassword",
                                                    venmo="testloginincorrectpassword"),
                               follow_redirects=True)

        response = client.post('/login', data=dict(email="testloginincorrectpassword@gmail.com", password="password1"))
        self.assertIn(b'Invalid email or password. Please try again.', response.data)
        person.delete_user("testloginincorrectpassword")
        person.remove_email_from_auth("testloginincorrectpassword@gmail.com", "password")

    def test_login_without_email(self):
        flask_app = create_app()
        client = flask_app.test_client()
        person.delete_user("testloginwithoutemail")
        person.remove_email_from_auth("testloginwithoutemail@gmail.com", "password")

        response = client.post('/signup', data=dict(email="testloginwithoutemail@gmail.com",
                                                    password="password",
                                                    username="testloginwithoutemail",
                                                    name="testloginwithoutemail",
                                                    venmo="testloginwithoutemail"),
                               follow_redirects=True)

        response = client.post('/login', data=dict(email="testloginwithoutemail", password="password"))
        self.assertIn(b'Invalid email or password. Please try again.', response.data)
        person.delete_user("testloginwithoutemail")
        person.remove_email_from_auth("testloginwithoutemail@gmail.com", "password")


class ApplicationSignupTestCase(unittest.TestCase):
    def test_signup_successful(self):
        flask_app = create_app()
        client = flask_app.test_client()
        person.delete_user("testcansignup")
        person.remove_email_from_auth("testcansignup@gmail.com", "password")

        response = client.post('/signup', data=dict(email="testcansignup@gmail.com",
                                                    password="password",
                                                    username="testcansignup",
                                                    name="testcansignup",
                                                    venmo="testcansignup"),
                               follow_redirects=True)
        self.assertIn(b'Remember me', response.data)
        person.delete_user("testcansignup")
        person.remove_email_from_auth("testcansignup@gmail.com", "password")

    def test_signup_existing_email(self):
        flask_app = create_app()
        client = flask_app.test_client()
        person.delete_user("testsignupexistingemail")
        person.remove_email_from_auth("testexistingemail@gmail.com", "password")

        response = client.post('/signup', data=dict(email="testexistingemail@gmail.com",
                                                    password="password",
                                                    username="testsignupexistingemail",
                                                    name="testsignupexistingemail1",
                                                    venmo="testsignupexistingemail1"),
                               follow_redirects=True)

        response = client.post('/signup', data=dict(email="testexistingemail@gmail.com",
                                                    password="password",
                                                    username="testsignupexistingemail2",
                                                    name="testsignupexistingemail2",
                                                    venmo="testsignupexistingemail2"),
                               follow_redirects=True)
        self.assertIn(b'Email already exists, please use a new email address to log in!', response.data)
        person.delete_user("testsignupexistingemail")
        person.remove_email_from_auth("testexistingemail@gmail.com", "password")

    def test_signup_existing_username(self):
        flask_app = create_app()
        client = flask_app.test_client()
        person.delete_user("testsignupexistingusername")
        person.remove_email_from_auth("testsignupexistingusername@gmail.com", "password")

        response = client.post('/signup', data=dict(email="testsignupexistingusername@gmail.com",
                                                    password="password",
                                                    username="testsignupexistingusername",
                                                    name="testsignupexistingusername",
                                                    venmo="testsignupexistingusername"),
                               follow_redirects=True)

        response = client.post('/signup', data=dict(email="testsignupexistingusername2@gmail.com",
                                                    password="password",
                                                    username="testsignupexistingusername",
                                                    name="testsignupexistingemail2",
                                                    venmo="testsignupexistingemail2"),
                               follow_redirects=True)
        self.assertIn(b'Username already exists.', response.data)
        person.delete_user("testsignupexistingusername")
        person.remove_email_from_auth("testsignupexistingusername@gmail.com", "password")


class ApplicationProfileTestCase(unittest.TestCase):
    def test_profile_can_access_own_profile(self):
        flask_app = create_app()
        client = flask_app.test_client()
        person.delete_user("testcanaccessownprofile")
        person.remove_email_from_auth("testcanaccessownprofile@gmail.com", "password")

        response = client.post('/signup', data=dict(email="testcanaccessownprofile@gmail.com",
                                                    password="password",
                                                    username="testcanaccessownprofile",
                                                    name="testcanaccessownprofile",
                                                    venmo="testcanaccessownprofile"),
                               follow_redirects=True)

        response = client.post('/login', data=dict(email="testcanaccessownprofile@gmail.com", password="password"),
                               follow_redirects=True)
        self.assertIn(b'test', response.data)
        self.assertIn(b'Click "+" to create a group!', response.data)
        person.delete_user("testcanaccessownprofile")
        person.remove_email_from_auth("testcanaccessownprofile@gmail.com", "password")

    def test_profile_cannot_access_other_profiles(self):
        flask_app = create_app()
        client = flask_app.test_client()

        with client.session_transaction() as session:
            session['is_logged'] = "testnotmyprofile"

        response = client.get('/profile/testsomeotherprofile', follow_redirects=True)
        self.assertIn(b'Unauthorized access. Please log in.', response.data)

    def test_choose_group(self):
        flask_app = create_app()
        client = flask_app.test_client()
        group.delete_group("testChooseGroup")
        person.delete_user("testChooseGroupMember")
        person.remove_email_from_auth("testChooseGroupMember@gmail.com", "password")
        with client.session_transaction() as session:
            session['is_logged'] = "test1"
            session['group_name'] = 'testChooseGroup'

        group_member = Person("testChooseGroupMember", "testChooseGroupMember",
                              "testChooseGroupMember@gmail.com", "testChooseGroupMember")
        response = client.post('/create_group', data=dict(group_name="testChooseGroup",
                                                          selected_members=['testChooseGroupMember']),
                               follow_redirects=True)

        response = client.get('/group', follow_redirects=True)
        self.assertIn(b'testChooseGroup', response.data)
        self.assertIn(b'Add Purchase', response.data)
        group.delete_group("testChooseGroup")
        person.delete_user("testChooseGroupMember")
        person.remove_email_from_auth("testChooseGroupMember@gmail.com", "password")

    def test_choose_group_post(self):
        flask_app = create_app()
        client = flask_app.test_client()
        group.delete_group("testChooseGroupPost")
        person.delete_user("testChooseGroupPostMember")
        person.remove_email_from_auth("testChooseGroupPostMember@gmail.com", "password")
        with client.session_transaction() as session:
            session['is_logged'] = "test1"

        group_member = Person("testChooseGroupPostMember", "testChooseGroupPostMember",
                              "testChooseGroupPostMember@gmail.com", "testChooseGroupPostMember")
        response = client.post('/create_group', data=dict(group_name="testChooseGroupPost",
                                                          selected_members=['testChooseGroupPostMember']),
                               follow_redirects=True)
        self.assertIn(b'testChooseGroupPost', response.data)

        response = client.post('/group', data=dict(select_group='testChooseGroupPost'), follow_redirects=True)
        self.assertIn(b'testChooseGroupPost', response.data)
        self.assertIn(b'Add Purchase', response.data)
        self.assertIn(b'testChooseGroupPostMember', response.data)

        group.delete_group("testChooseGroupPost")
        person.delete_user("testChooseGroupPostMember")
        person.remove_email_from_auth("testChooseGroupPostMember@gmail.com", "password")

    def test_create_group(self):
        flask_app = create_app()
        client = flask_app.test_client()
        with client.session_transaction() as session:
            session['is_logged'] = "test1"

        response = client.get('/create_group', data=dict(username="test1"), follow_redirects=True)
        self.assertIn(b'Create a Group', response.data)
        self.assertIn(b'test1', response.data)

    def test_create_group_post(self):
        flask_app = create_app()
        client = flask_app.test_client()
        group.delete_group("testCreateGroupPost")
        person.delete_user("testCreateGroupPostMember")
        person.remove_email_from_auth("testCreateGroupPostMember@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = "test1"

        group_member = Person("testCreateGroupPostMember", "testCreateGroupPostMember",
                              "testCreateGroupPostMember@gmail.com", "testCreateGroupPostMember")
        response = client.post('/create_group', data=dict(group_name="testCreateGroupPost",
                                                          selected_members=['testCreateGroupPostMember']),
                               follow_redirects=True)
        self.assertIn(b'testCreateGroupPost', response.data)
        group.delete_group("testCreateGroupPost")
        person.delete_user("testCreateGroupPostMember")
        person.remove_email_from_auth("testCreateGroupPostMember@gmail.com", "password")

    def test_add_purchase(self):
        flask_app = create_app()
        client = flask_app.test_client()
        group.delete_group("testAddPurchase")
        person.delete_user("testAddPurchaseMember")
        person.remove_email_from_auth("testAddPurchaseMember@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'test1'
            session['group_name'] = 'testAddPurchase'

        group_member = Person("testAddPurchaseMember", "testAddPurchaseMember",
                              "testAddPurchaseMember@gmail.com", "testAddPurchaseMember")
        response = client.post('/create_group', data=dict(group_name="testAddPurchase",
                                                          selected_members=['testAddPurchaseMember']),
                               follow_redirects=True)
        response = client.get('/add_purchase', follow_redirects=True)
        self.assertIn(b'Add a Purchase', response.data)
        group.delete_group("testAddPurchase")
        person.delete_user("testAddPurchaseMember")
        person.remove_email_from_auth("testAddPurchaseMember@gmail.com", "password")

    def test_add_purchase_post(self):
        flask_app = create_app()
        client = flask_app.test_client()
        group.delete_group("testAddPurchasePost")
        person.delete_user("testAddPurchasePostMember")
        person.remove_email_from_auth("testAddPurchasePostMember@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'test1'
            session['group_name'] = 'testAddPurchasePost'

        group_member = Person("testAddPurchasePostMember", "testAddPurchasePostMember",
                              "testAddPurchasePostMember@gmail.com", "testAddPurchasePostMember")
        response = client.post('/create_group', data=dict(group_name="testAddPurchasePost",
                                                          selected_members=['testAddPurchasePostMember']),
                               follow_redirects=True)

        response = client.post('/add_purchase', data=dict(item="testItem",
                                                          price=1.23,
                                                          test1=50,
                                                          testAddPurchasePostMember=50),
                               follow_redirects=True)
        self.assertIn(b'<b>Buyer: </b>test1', response.data)
        self.assertIn(b'<b>Item: </b>testItem', response.data)
        self.assertIn(b'<b>Cost: </b>1.23', response.data)
        group.delete_group("testAddPurchasePost")
        person.delete_user("testAddPurchasePostMember")
        person.remove_email_from_auth("testAddPurchasePostMember@gmail.com", "password")
    
    def test_add_purchase_post_with_image(self):
        flask_app = create_app()
        client = flask_app.test_client()
        group.delete_group("testAddPurchasePost")
        person.delete_user("testAddPurchasePostMember")
        person.remove_email_from_auth("testAddPurchasePostMember@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'test1'
            session['group_name'] = 'testAddPurchasePost'
        
        group_member = Person("testAddPurchasePostMember", "testAddPurchasePostMember", 
                        "testAddPurchasePostMember@gmail.com", "testAddPurchasePostMember")
        response = client.post('/create_group', data=dict(group_name="testAddPurchasePost",
                                                          selected_members=['testAddPurchasePostMember']),
                               follow_redirects=True)
        
        response = client.post('/add_purchase', data=dict(image=(io.BytesIO(b"test bytes"), 'test.jpg'),
                                                            item="testItem",
                                                            price=1.23,
                                                            test1=50,
                                                            testAddPurchasePostMember=50),
                               follow_redirects=True)

        self.assertIn(b'<b>Buyer: </b>test1', response.data)
        self.assertIn(b'<b>Item: </b>testItem', response.data)
        self.assertIn(b'<b>Cost: </b>1.23', response.data)
        group.delete_group("testAddPurchasePost")
        person.delete_user("testAddPurchasePostMember")
        person.remove_email_from_auth("testAddPurchasePostMember@gmail.com", "password")
    
    def test_add_purchase_post_splits_not_100(self):
        flask_app = create_app()
        client = flask_app.test_client()
        group.delete_group("testAddPurchasePost")
        person.delete_user("testAddPurchasePostMember")
        person.remove_email_from_auth("testAddPurchasePostMember@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'test1'
            session['group_name'] = 'testAddPurchasePost'

        group_member = Person("testAddPurchasePostMember", "testAddPurchasePostMember",
                              "testAddPurchasePostMember@gmail.com", "testAddPurchasePostMember")
        response = client.post('/create_group', data=dict(group_name="testAddPurchasePost",
                                                          selected_members=['testAddPurchasePostMember']),
                               follow_redirects=True)

        response = client.post('/add_purchase', data=dict(item="testItem",
                                                          price=1.23,
                                                          test1=50,
                                                          testAddPurchasePostMember=49),
                               follow_redirects=True)
        self.assertIn(b'Add a Purchase', response.data)
        group.delete_group("testAddPurchasePost")
        person.delete_user("testAddPurchasePostMember")
        person.remove_email_from_auth("testAddPurchasePostMember@gmail.com", "password")

    def test_logout(self):
        flask_app = create_app()
        client = flask_app.test_client()

        response = client.get('/logout', follow_redirects=True)
        self.assertIn(b'Remember me', response.data)

    def test_settings(self):
        flask_app = create_app()
        client = flask_app.test_client()

        with client.session_transaction() as session:
            session['is_logged'] = 'test1'

        response = client.get('/settings', follow_redirects=True)
        self.assertIn(b'Settings', response.data)

    def test_venmo_display(self):
        flask_app = create_app()
        client = flask_app.test_client()

        with client.session_transaction() as session:
            session['is_logged'] = 'test1'
            session['group_name'] = 'testVenmoDisplayGroup'

        group_member = Person("testVenmoDisplay", "testVenmoDisplay",
                              "testVenmoDisplay@gmail.com", "testVenmoDisplayVENMO")
        response = client.post('/create_group', data=dict(group_name="testVenmoDisplayGroup",
                                                          selected_members=['testVenmoDisplay']),
                               follow_redirects=True)
        response = client.get('/group', follow_redirects=True)
        self.assertIn(b'testVenmoDisplay', response.data)
        self.assertIn(b'Venmo: </b>testVenmoDisplayVENMO', response.data)

        group.delete_group("testVenmoDisplayGroup")
        person.delete_user("testVenmoDisplay")
        person.remove_email_from_auth("testVenmoDisplay@gmail.com", "password")

    def test_balance(self):
        flask_app = create_app()
        client = flask_app.test_client()

        with client.session_transaction() as session:
            session['is_logged'] = 'test1'

        response = client.get('/balance', follow_redirects=True)
        self.assertIn(b'Your Balance is:', response.data)

    def test_get_venmo(self):
        flask_app = create_app()
        client = flask_app.test_client()
        group.delete_group("groupGetVenmo")
        person.delete_user("testGetVenmoMember")
        person.remove_email_from_auth("testGetVenmoMember@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'test1'
            session['group_name'] = 'groupGetVenmo'

        group_member = Person("testGetVenmoMember", "testGetVenmoMember",
                              "testGetVenmoMember@gmail.com", "testGetVenmoMember")
        response = client.post('/create_group', data=dict(group_name="groupGetVenmo",
                                                          selected_members=['testGetVenmoMember']),
                               follow_redirects=True)
        response = client.get('/get_venmo', follow_redirects=True)
        self.assertIn(b'List of Venmo Transactions For Group:', response.data)
        group.delete_group("groupGetVenmo")
        person.delete_user("testGetVenmoMember")
        person.remove_email_from_auth("testGetVenmoMember@gmail.com", "password")

    def test_leave_group(self):
        flask_app = create_app()
        client = flask_app.test_client()

        group.delete_group("testLeaveGroupGroup")
        person.delete_user("testLeaveGroup")
        person.remove_email_from_auth("testLeaveGroup@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'testLeaveGroup'
            session['group_name'] = 'testLeaveGroupGroup'

        group_member = Person("testLeaveGroup", "testLeaveGroup",
                              "testLeaveGroup@gmail.com", "testLeaveGroup")
        response = client.get('/leave_group',
                              follow_redirects=True)

        self.assertIn(b'Would you, testLeaveGroup, like to leave group testLeaveGroupGroup?', response.data)
        group.delete_group("testLeaveGroupGroup")
        person.delete_user("testLeaveGroup")
        person.remove_email_from_auth("testLeaveGroup@gmail.com", "password")

    def test_leave_group_user_get(self):
        flask_app = create_app()
        client = flask_app.test_client()

        group.delete_group("testLeaveGroupUserGroup")
        person.delete_user("testLeaveGroupUser")
        person.remove_email_from_auth("testLeaveGroupUser@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'testLeaveGroupUser'
            session['group_name'] = 'testLeaveGroupUserGroup'

        group_member = Person("testLeaveGroupUser", "testLeaveGroupUser",
                              "testLeaveGroupUser@gmail.com", "testLeaveGroupUser")
        response = client.get('/leave_group_user',
                              follow_redirects=True)

        self.assertIn(b'<h5 class="text-right" id="brand">testLeaveGroupUser</h5>', response.data)
        group.delete_group("testLeaveGroupUserGroup")
        person.delete_user("testLeaveGroupUser")
        person.remove_email_from_auth("testLeaveGroupUser@gmail.com", "password")

    def test_leave_group_user_post(self):
        flask_app = create_app()
        client = flask_app.test_client()

        group.delete_group("testLeaveGroupUserGroup")
        person.delete_user("testLeaveGroupUser")
        person.remove_email_from_auth("testLeaveGroupUser@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'testLeaveGroupUser'
            session['group_name'] = 'testLeaveGroupUserGroup'

        group_member = Person("testLeaveGroupUser", "testLeaveGroupUser",
                              "testLeaveGroupUser@gmail.com", "testLeaveGroupUser")
        group_member_2 = Person("testLeaveGroupUser2", "testLeaveGroupUser2",
                                "testLeaveGroupUser2@gmail.com", "testLeaveGroupUser2")

        response = client.post('/create_group', data=dict(group_name="testLeaveGroupUserGroup",
                                                          selected_members=['testLeaveGroupUser2']),
                               follow_redirects=True)

        self.assertEqual(["testLeaveGroupUser", "testLeaveGroupUser2"],
                         group.get_all_users_in_group("testLeaveGroupUserGroup"))
        response = client.post('/leave_group_user',
                               follow_redirects=True)

        self.assertIn(b'<h5 class="text-right" id="brand">testLeaveGroupUser</h5>', response.data)
        self.assertEqual(["testLeaveGroupUser2"], group.get_all_users_in_group("testLeaveGroupUserGroup"))
        group.delete_group("testLeaveGroupUserGroup")
        person.delete_user("testLeaveGroupUser")
        person.delete_user("testLeaveGroupUser2")
        person.remove_email_from_auth("testLeaveGroupUser@gmail.com", "password")

    def test_delete_user(self):
        flask_app = create_app()
        client = flask_app.test_client()

        group.delete_group("testLeaveGroupUserGroup")
        person.delete_user("testDeleteUser")
        person.remove_email_from_auth("testDeleteUser@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'testDeleteUser'

        user = Person("testDeleteUser", "testDeleteUser",
                      "testDeleteUser@gmail.com", "testDeleteUser")

        response = client.get('/delete_user', follow_redirects=True)
        self.assertIn(b'Sign Up', response.data)

    def test_delete_all_purchases(self):
        flask_app = create_app()
        client = flask_app.test_client()

        group.delete_group("testLeaveGroupUserGroup")
        person.delete_user("testDeleteUser")
        person.remove_email_from_auth("testDeleteUser@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'testDeleteAllPurchases'
            session['group_name'] = 'testDeleteAllPurchasesGroup'

        group_member = Person("testDeleteAllPurchases", "testDeleteAllPurchases",
                              "testDeleteAllPurchases@gmail.com", "testDeleteAllPurchases")
        group_member_2 = Person("testDeleteAllPurchases2", "testDeleteAllPurchases2",
                                "testDeleteAllPurchases2@gmail.com", "testDeleteAllPurchases2")

        response = client.post('/create_group', data=dict(group_name="testDeleteAllPurchasesGroup",
                                                          selected_members=['testDeleteAllPurchases2']),
                               follow_redirects=True)

        response = client.post('/add_purchase', data=dict(item="testItem",
                                                          price=1.23,
                                                          testDeleteAllPurchases=50,
                                                          testDeleteAllPurchases2=50),
                               follow_redirects=True)

        self.assertEqual((['testItem'],
                          ['testDeleteAllPurchases'],
                          ['1.23']),
                         group.get_all_purchases_for_group("testDeleteAllPurchasesGroup"))

        response = client.post('/add_purchase', data=dict(item="testItem2",
                                                          price=1.24,
                                                          testDeleteAllPurchases=50,
                                                          testDeleteAllPurchases2=50),
                               follow_redirects=True)
        self.assertEqual((['testItem', 'testItem2'],
                          ['testDeleteAllPurchases', 'testDeleteAllPurchases'],
                          ['1.23', '1.24']),
                         group.get_all_purchases_for_group("testDeleteAllPurchasesGroup"))

        response = client.post('/delete_all_purchases', follow_redirects=True)
        self.assertEqual(([], [], []),
                         group.get_all_purchases_for_group("testDeleteAllPurchasesGroup"))

        group.delete_group("testDeleteAllPurchasesGroup")
        person.delete_user("testDeleteAllPurchases")
        person.delete_user("testDeleteAllPurchases2")
        person.remove_email_from_auth("testDeleteAllPurchases@gmail.com", "password")
        person.remove_email_from_auth("testDeleteAllPurchases2@gmail.com", "password")

    def test_delete_purchase(self):
        flask_app = create_app()
        client = flask_app.test_client()

        group.delete_group("testDeletePurchaseGroup")
        person.delete_user("testDeletePurchase")
        person.remove_email_from_auth("testDeletePurchase@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'testDeletePurchase'
            session['group_name'] = 'testDeletePurchaseGroup'

        group_member = Person("testDeletePurchase", "testDeletePurchase",
                              "testDeletePurchase@gmail.com", "testDeletePurchase")
        group_member_2 = Person("testDeletePurchase2", "testDeletePurchase2",
                                "testDeletePurchase2@gmail.com", "testDeletePurchase2")

        response = client.post('/create_group', data=dict(group_name="testDeletePurchaseGroup",
                                                          selected_members=['testDeletePurchase2']),
                               follow_redirects=True)

        response = client.post('/add_purchase', data=dict(item="testItem",
                                                          price=1.23,
                                                          testDeletePurchase=50,
                                                          testDeletePurchase2=50),
                               follow_redirects=True)

        self.assertEqual((['testItem'],
                          ['testDeletePurchase'],
                          ['1.23']),
                         group.get_all_purchases_for_group("testDeletePurchaseGroup"))

        response = client.post('/add_purchase', data=dict(item="testItem2",
                                                          price=1.24,
                                                          testDeletePurchase=50,
                                                          testDeletePurchase2=50),
                               follow_redirects=True)
        self.assertEqual((['testItem', 'testItem2'],
                          ['testDeletePurchase', 'testDeletePurchase'],
                          ['1.23', '1.24']),
                         group.get_all_purchases_for_group("testDeletePurchaseGroup"))

        response = client.post('/delete_purchase', data=dict(item_name="testItem"),
                               follow_redirects=True)
        self.assertEqual((['testItem2'],
                          ['testDeletePurchase'],
                          ['1.24']),
                         group.get_all_purchases_for_group("testDeletePurchaseGroup"))

        group.delete_group("testDeletePurchaseGroup")
        person.delete_user("testDeletePurchase")
        person.delete_user("testDeletePurchase2")
        person.remove_email_from_auth("testDeletePurchase@gmail.com", "password")
        person.remove_email_from_auth("testDeletePurchase2@gmail.com", "password")
    
    def test_add_profile_picture(self):
        flask_app = create_app()
        client = flask_app.test_client()

        person.delete_user("testAddProfilePicture")
        person.remove_email_from_auth("testAddProfilePicture@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'testAddProfilePicture'
        
        group_member = Person("testAddProfilePicture", "testAddProfilePicture", 
                        "testAddProfilePicture@gmail.com", "testAddProfilePicture")
                    
        response = client.post("/add_profile_picture", 
                                data=dict(image=(io.BytesIO(b"test bytes"), 'test.jpg')),
                                follow_redirects=True)
                
        self.assertIn(b'testAddProfilePicture_profile_picture.JPG', response.data)
        person.delete_user("testAddProfilePicture")
        person.remove_email_from_auth("testAddProfilePicture@gmail.com", "password")
    
    def test_add_group_picture(self):
        flask_app = create_app()
        client = flask_app.test_client()

        group.delete_group("testAddGroupPictureGroup")
        person.delete_user("testAddGroupPicture")
        person.remove_email_from_auth("testAddGroupPicture@gmail.com", "password")

        with client.session_transaction() as session:
            session['is_logged'] = 'testAddGroupPicture'
            session['group_name'] = 'testAddGroupPictureGroup'
        
        group_member = Person("testAddGroupPicture", "testAddGroupPicture", 
                        "testAddGroupPicture@gmail.com", "testAddGroupPicture")
        group_member_2 = Person("testAddGroupPicture2", "testAddGroupPicture2", 
        "testAddGroupPicture2@gmail.com", "testAddGroupPicture2")
                        
        response = client.post('/create_group', data=dict(group_name="testAddGroupPictureGroup",
                                            selected_members=['testAddGroupPicture2']),
                                follow_redirects=True)
                    
        response = client.post("/add_group_picture", 
                                data=dict(image=(io.BytesIO(b"test bytes"), 'test.jpg')),
                                follow_redirects=True)
                
        self.assertIn(b'testAddGroupPictureGroup_group_picture.JPG', response.data)

        group.delete_group("testAddGroupPictureGroup")
        person.delete_user("testAddProfilePicture")
        person.delete_user("testAddProfilePicture2")
        person.remove_email_from_auth("testAddProfilePicture@gmail.com", "password")
        person.remove_email_from_auth("testAddProfilePicture2@gmail.com", "password")

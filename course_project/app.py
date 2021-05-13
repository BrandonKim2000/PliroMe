from flask import Flask, request, render_template, redirect, url_for, session
from course_project import login_system, group, person, purchase
import os
import tempfile
from venmo_api import Client

"""This file contains all of our functions that are currently exposed to Flask, wrapping them with the functions 
necessary in order to create and produce working HTML templates alongside them"""


def create_app() -> Flask:
    """This function starts the application process, which will run different functions defined within this main one
    in order to translate to inputs, button clicks, and pages viewed on the HTML page

    :return: (flask_app) Which includes the information about the current folder, key, and debug options are running via
    Flask"""
    flask_app = Flask(__name__)
    flask_app.debug = True
    flask_app.static_folder = 'static'
    flask_app.secret_key = 'the random string'

    # functions here
    @flask_app.route('/', methods=['GET'])
    def index() -> bytes:
        """This function relates to the start of the screen, whether that be the login information was already inputted
        with 'remember me' being pressed (which would take the user straight to their home page), or it would launch
        the initial login form page

        :return: (HTML) The associated page related to the given functionality at the time (logging in for the first time
        vs the 'remember me' feature)"""
        if 'username' in session:
            return redirect(url_for('profile', username=session['username']))
        return render_template("login.html")

    @flask_app.route('/login', methods=['GET', 'POST'])
    def login() -> bytes:
        """Logs the user through the HTML and allows the application to transition to the next step of the process, whether
        it be to show the user their profile information or display the login page again with an error

        :return: (HTML) The specific page based on the functionality given (Either the profile page or the login page)"""
        error = None
        success = None

        # Provide error and success with values
        if 'msg_at_login_good' in session:
            success = session['msg_at_login_good']
            session.pop('msg_at_login_good', None)
        if 'msg_at_login_bad' in session:
            error = session['msg_at_login_bad']
            session.pop('msg_at_login_bad', None)

        # Check to see if user inputted info is valid for login
        if request.method == 'POST':
            session.pop('msg_at_login_good', None)
            session.pop('msg_at_login_bad', None)
            # get email, password, and remember me
            email = request.form['email']
            password = request.form['password']
            remember = True if request.form.get("remember") else False
            response = login_system.login(email, password)
            if response['error_code'] == 1:
                error = response['msg']
            else:
                # Handles the processes of "remember me" when the user is signing in to the group
                if remember:
                    session['username'] = response['username']
                session['is_logged'] = response['username']
                username = response['username']
                all_user_groups = group.get_all_user_groups(username)
                # open up the profile page
                return redirect(url_for('profile', username=username, all_user_groups=all_user_groups))

        return render_template("login.html", error=error, success=success)

    @flask_app.route('/signup', methods=['GET', 'POST'])
    def signup() -> bytes:
        """This function defines the signup page for the user. This form has the user input their name, email,
        username, password, and venmo information. Once complete, it will redirect them to the option to log in to their
        newly signed up account

        :return: (HTML) Either the login page for the user to login in with their information, or the signup page again
        with the given error that occurred which halted them from signing up"""
        error = None
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            venmo = request.form['venmo']

            response = login_system.sign_up(email, password, name, username, venmo)
            msg = response['msg']
            if response['error_code'] == 1:
                return render_template('signup.html', msg=msg)
            else:
                # login successful, go back to the main page
                session['msg_at_login_good'] = "Account successfully created! Log in now."
                return redirect(url_for('login'))
        return render_template('signup.html', msg=None)

    # Take user to their profile by redirecting the url
    @flask_app.route('/profile', methods=['GET'])
    def profile() -> bytes:
        """This function defines the basic profile page initialization, redirects the profile page for the specific user

        :return: (HTML) Redirects the user to their specific profile page"""
        username = session['is_logged']
        return redirect(url_for('profile_user', username=username))

    # Check if redirect url is valid, otherwise provide information pertaining to the user
    @flask_app.route('/profile/<username>', methods=['GET', 'POST'])
    def profile_user(username: str) -> bytes:
        """This function checks first to make sure that the user is loggin in and currently in an available session.
        If the user is not in the current session then you will be redirected to the login page to retry logging in.
        Otherwise, the user will be able to view their specific HTML page with the specific user information that they
        contain in their database.

        :return: (HTML) Either the login page due to an error, or the profile page displaying the user's specific
        information"""
        # if error, go back to the login page.
        if 'is_logged' not in session or session['is_logged'] != username:
            session['msg_at_login_bad'] = "Unauthorized access. Please log in."
            session.pop('is_logged', None)
            session.pop('username', None)
            return redirect(url_for('login'))
        else:
            # go to the profile page
            all_user_groups = group.get_all_user_groups(username)
            if person.has_profile_picture(username):
                profile_picture_link = person.get_profile_picture(username)
            else:
                profile_picture_link = person.get_default_profile_picture()
            return render_template('profile.html', username=username, all_user_groups=all_user_groups,
                                   pic=profile_picture_link)

    # Provide a page to the user where they can see their group using their session or request
    @flask_app.route('/group', methods=['GET', 'POST'])
    def choose_group() -> bytes:
        """This group is the form that allows the user to choose a specific group to look at once they have become a
        member of a group

        :return: (HTML) Page allowing the user to click on the specific group they want to view, and clicking a button
        will redirect them to viewing the group's specific information"""
        username = session['is_logged']
        # show up the choose group page.
        if request.method == 'GET':
            group_name = session['group_name']
            all_group_members = group.get_all_users_in_group(group_name)
            items, buyers, prices = group.get_all_purchases_for_group(group_name)
            venmos = group.get_all_venmos_in_group(group_name)
            num_items = len(items)
            num_people = len(all_group_members)
            group_recipts_links = group.get_recipts(group_name)
            if group.has_group_picture(group_name):
                group_picture_link = group.get_group_picture(group_name)
            else:
                group_picture_link = group.get_default_group_picture()
            return render_template('group.html', username=username, venmos=venmos, num_people=num_people,
                                   group_name=group_name, group_members=all_group_members,
                                   items=items, buyers=buyers, prices=prices, num=num_items,
                                   img_links=group_recipts_links, pic=group_picture_link)
        elif request.method == 'POST':
            group_name = request.form['select_group']
            session['group_name'] = group_name
            all_group_members = group.get_all_users_in_group(group_name)
            items, buyers, prices = group.get_all_purchases_for_group(group_name)
            venmos = group.get_all_venmos_in_group(group_name)
            num_items = len(items)
            num_people = len(all_group_members)
            group_recipts_links = group.get_recipts(group_name)
            if group.has_group_picture(group_name):
                group_picture_link = group.get_group_picture(group_name)
            else:
                group_picture_link = group.get_default_group_picture()
            return render_template('group.html', username=username, venmos=venmos, num_people=num_people,
                                   group_name=group_name, group_members=all_group_members,
                                   items=items, buyers=buyers, prices=prices, num=num_items,
                                   img_links=group_recipts_links, pic=group_picture_link)

    @flask_app.route('/add_profile_picture', methods=['GET', 'POST'])
    def add_profile_picture() -> bytes:
        """ Adds a profile picture for a specific user

        :return: (HTML) Will return to the profile page, and you will be able to see the added profile picture
        """
        # get the person image
        username = session['is_logged']
        if 'image' in request.files:
            image = request.files['image']
            temp = tempfile.NamedTemporaryFile(delete=False)
            image.save(temp.name)
            person.add_profile_picture(temp.name, username)

            temp.close()
            os.remove(temp.name)

        return redirect(url_for('profile_user', username=username))

    @flask_app.route('/add_group_picture', methods=['GET', 'POST'])
    def add_group_picture() -> bytes:
        """ Adds a group picture for a specific group

        :return: (HTML) Will return to the group page, and you will be able to see the added group picture
        """
        # get the group image
        group_name = session['group_name']

        if 'image' in request.files:
            image = request.files['image']
            temp = tempfile.NamedTemporaryFile(delete=False)
            image.save(temp.name)
            group.add_group_picture(temp.name, group_name)

            temp.close()
            os.remove(temp.name)

        return redirect(url_for('choose_group'))

    # Create a new group after validating the users login
    # Groups are created by providing a template as a GET or POSTing the input information
    @flask_app.route('/create_group', methods=['GET', 'POST'])
    def create_group() -> bytes:
        """This function defines the process for creating a group, allowing a specific user to create the name of
        the group and add specific members to that group

        :return: (HTML) Will return to the profile page, and you will be able to see that group in the dropdown menu
        to choose a specific group to look at"""
        username = session['is_logged']
        all_users = group.get_all_users()
        all_users.remove(username)
        # if loading the page, just show the create group page
        if request.method == 'GET':
            return render_template('create_group.html', username=username, all_users=all_users)
        if request.method == 'POST':
            # add the new group and the selected members to a group and go back to the profile page
            group_name = request.form['group_name']
            selected_members = list(request.form.getlist("selected_members"))

            new_group = group.Group(group_name)
            new_group.add_member(username)

            for member in selected_members:
                new_group.add_member(member)

            return redirect(url_for('profile', username=username))

    # Provide a template and redirect based on if a user needs to input a purchase or submit a purchase
    @flask_app.route('/add_purchase', methods=['GET', 'POST'])
    def add_purchase() -> bytes:
        """This functions defines the process for adding a purchase to a specific group. The user will add the name
        of the item and the price, and it will become associated with that specific user and be posted to the group page

        :return: (HTML) Will redirect the user back to the group page with the updated purchase added in a column"""
        username = session['is_logged']
        group_name = session['group_name']
        # if loading the page, get the add_purchase page
        if request.method == 'GET':
            group_members = group.get_all_users_in_group(group_name)
            return render_template('add_purchase.html', username=username, group_name=group_name,
                                   group_members=group_members, auto_percent=100 / len(group_members))
        elif request.method == 'POST':
            # add the purchase with the item and price
            item = request.form['item']
            price = request.form['price']

            # get the receipt image
            if 'image' in request.files:
                image = request.files['image']
                temp = tempfile.NamedTemporaryFile(delete=False)
                image.save(temp.name)
                group.add_receipt(temp.name, group_name)

                temp.close()
                os.remove(temp.name)

            # do the splitting algorithm
            group_members = group.get_all_users_in_group(group_name)
            num_members = len(group_members)
            group_percentage = {}
            sum_percentages = 0

            # Handles the process of splitting purchases and returning the correct HTML template
            for member in group_members:
                group_percentage[member] = request.form[member]
                sum_percentages += int(float(group_percentage[member]))
            if sum_percentages == 100:
                purchase.Purchase(username, group_name, item, price, group_percentage)
                return redirect(url_for('choose_group'))
            else:
                return render_template('add_purchase.html', username=username, group_name=group_name,
                                       group_members=group_members, auto_percent=100 / len(group_members))

    @flask_app.route('/logout', methods=['GET'])
    def logout() -> bytes:
        """This function logs out the specific user from PliroMe

        :return: (HTML) Returns back to the login page for users to either sign up with a new account or log in"""
        session.pop('username', None)
        session.pop('user_id', None)
        session.pop('is_logged', None)
        login_system.logout()
        return redirect(url_for('index'))

    # Take a user to the contact us page
    @flask_app.route('/balance', methods=['GET', 'POST'])
    def balance() -> bytes:
        """This function defines the processes that handle the "balance" page on the PliroMe website

        :return: (HTML) Redirects the user to the "balance" page on PliroMe"""
        if 'is_logged' in session:
            username = session['is_logged']
            user_balance = person.get_user_balance(username)
            if user_balance is None:
                user_balance = 0
            return render_template('balance.html', username=username, balance=user_balance)

    # Take a user to their settings
    @flask_app.route('/settings', methods=['GET'])
    def settings() -> bytes:
        """This function defines the processes that handle the "settings" page on the PliroMe website

        :return: (HTML) Redirects the user to the "settings" page on PliroMe"""
        if 'is_logged' in session:
            username = session['is_logged']
            return render_template('settings.html', username=username)

    @flask_app.route('/venmo_settings', methods=['GET'])
    def venmo_settings() -> bytes:
        """This function defines the processes that takes the user to the Venmo settings page

        :return: (HTML) Redirects the user to the "settings" page on PliroMe"""
        if 'is_logged' in session:
            username = session['is_logged']
            return render_template('venmo_settings.html', username=username)

    @flask_app.route('/get_access_token', methods=['POST'])
    def get_access_token() -> bytes:
        """This function defines the processes that let the user get their Venmo access token

        :return: (HTML) Redirects the user to the "settings" page on PliroMe"""
        if 'is_logged' in session:
            username = session['is_logged']
            email = request.form["email"]
            password = request.form["password"]
            person.get_access_token(username, email, password)
            return render_template('settings.html', username=username)

    @flask_app.route('/get_venmo', methods=['GET', 'POST'])
    def get_venmo() -> bytes:
        """This function defines the processes that handle the button that returns to the user the list of venmo
        transactions that need to be completed within a specific group

        :return: (HTML) Redirects the user to a page that gives them the list of transactions"""
        if 'is_logged' in session:
            username = session['is_logged']
            group_name = session['group_name']
            send_venmos = False
            if request.method == 'POST':
                if "sendVenmos" in request.form and request.form["sendVenmos"]:
                    send_venmos = True
            group_venmos = group.split_purchases(group_name, send_venmos)
            return render_template('get_venmo.html', username=username, group=group_name, transactions=group_venmos)

    @flask_app.route('/delete_purchase', methods=['GET', 'POST'])
    def delete_purchase() -> bytes:
        """This function defines the processes that handle deleting a purchase from a group

        :return: (HTML) Redirects the user to a confirmation page to leave their group, and then back to the profile page
        """
        if 'is_logged' in session:
            username = session['is_logged']
            group_name = session['group_name']
            purchase = request.form['item_name']
            group.delete_purchase(group_name, purchase)
            all_group_members = group.get_all_users_in_group(group_name)
            items, buyers, prices = group.get_all_purchases_for_group(group_name)
            venmos = group.get_all_venmos_in_group(group_name)
            num_items = len(items)
            num_people = len(all_group_members)
            group_recipts_links = group.get_recipts(group_name)
            return render_template('group.html', username=username, venmos=venmos, num_people=num_people,
                                   group_name=group_name, group_members=all_group_members,
                                   items=items, buyers=buyers, prices=prices, num=num_items,
                                   img_links=group_recipts_links)

    @flask_app.route('/delete_all_purchases', methods=['GET', 'POST'])
    def delete_all_purchases() -> bytes:
        """This function defines the processes that handle deleting a purchase from a group

        :return: (HTML) Redirects the user to a confirmation page to leave their group, and then back to the profile page
        """
        if 'is_logged' in session:
            username = session['is_logged']
            group_name = session['group_name']
            group.delete_all_purchases(group_name)
            all_group_members = group.get_all_users_in_group(group_name)
            items, buyers, prices = group.get_all_purchases_for_group(group_name)
            venmos = group.get_all_venmos_in_group(group_name)
            num_items = len(items)
            num_people = len(all_group_members)
            group_recipts_links = group.get_recipts(group_name)
            return render_template('group.html', username=username, venmos=venmos, num_people=num_people,
                                   group_name=group_name, group_members=all_group_members,
                                   items=items, buyers=buyers, prices=prices, num=num_items,
                                   img_links=group_recipts_links)

    @flask_app.route('/leave_group', methods=['GET', 'POST'])
    def leave_group() -> bytes:
        """This function defines the processes that handle the button that allows the user to leave a specific group

        :return: (HTML) Redirects the user to a confirmation page to leave their group,
        and then back to the profile page
        """
        if 'is_logged' in session:
            username = session['is_logged']
            group_name = session['group_name']
            return render_template('leave_group.html', username=username, group=group_name)

    @flask_app.route('/delete_user', methods=['GET', 'POST'])
    def delete_user() -> bytes:
        """
        This function deletes a user from all their groups then deletes the user from the database

        :return: (HTML) Redirects the user to the login page
        """
        if 'is_logged' in session:
            username = session['is_logged']
            all_user_groups = group.get_all_user_groups(username)
            for group_name in all_user_groups:
                group.leave_group(username, group_name)
            person.delete_user(username)
            return redirect(url_for('login'))

    @flask_app.route('/leave_group_user', methods=['GET', 'POST'])
    def leave_group_user() -> bytes:
        """This function defines the confirmation page prior to leaving a group

        :return: (HTML) The correct page depending on if they hit confirm or cancel
        """
        username = session['is_logged']
        group_name = session['group_name']
        if request.method == "GET":
            if 'is_logged' in session:
                all_user_groups = group.get_all_user_groups(username)
                return render_template('profile.html', username=username, all_user_groups=all_user_groups)
        elif request.method == "POST":
            if 'is_logged' in session:
                group.leave_group(group_name, username)
                all_user_groups = group.get_all_user_groups(username)
                return render_template('profile.html', username=username, all_user_groups=all_user_groups)

    return flask_app

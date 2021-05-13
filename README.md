# PliroMe: A Group Payment Management System
## Team Members: 
- Brandon Kim: Completed the task for leaving a group, made the YouTube tutorial, and added to the User Documentation.
- Adit Gupta:  Worked with Jonathan to complete UI advancements, group profile pictures, user profile pictures, and tests.
- Benny Beinish: Completed the Venmo functionality and UI, as well as writing tests.
- Jonathan Nam: Worked with Adit to complete UI advancements, group profile pictures, user profile pictures, and tests.
- Camden Masters: Completed the tasks that are associated with the security of our config file.
- Sergio Quispe: Completed the tasks that are associated with deploying our website to the cloud in order to be accessed via link.
- William Faoro: Completed the tasks associated with deleting your account within the UI.
## Team Member Contribution:
- Brandon Kim: 20%
- Adit Gupta: 18.29%
- Benny Beinish: 18.43%
- Jonathan Nam: 16.86%
- Camden Masters: 4.29%
- Sergio Quispe: 14.29%
- William Faoro: 7.86%

To see how we split the contributions, please look at [Google Spreadsheet](https://docs.google.com/spreadsheets/d/182L10lo2K45c7zMFrXt0P9l8N305lkIwqEZFuR1gzLk/edit#gid=941578423)

### Version 3.0; Last Edited 5/11/2021

## * Accessing the Application via Internet
With our final sprint delivery, Sergio was able to connect our application to the cloud utilizing Amazon and EC2, so you may now access the PliroMe application by visiting the link provided below. 

[PliroMe Web Application](http://ec2-3-140-184-85.us-east-2.compute.amazonaws.com/)

**NOTE: You will not have to utilize Docker or Git if you are simply going to the link that we provide for you**


## * How to Install the Program on your Computer
This section will describe how to install the program on your local computer. Because we are completing our work through Gitlab, there will be two main techniques in downloading the program to a local hardware system. The product can either be run through Docker or can be run by manually installing the requirements and running flask. 

### Using Docker to run the Project
Assuming that you already have Docker installed on your machine, this project can be run very simply by running a couple docker commands. Change directory to the folder which contains the Dockerfile (course-project).

The commands are:

 docker build -t course_project:plirome .

 docker run -it --rm -p 5000:5000 course_project:plirome

After using these commands, click on the url generated and proceed to using the web app. 

**NOTE: If you run these commands, you should not need to use any other instructions in order to run the project**

### Manually Downloading the Project 
When you go to the “Project Overview” page on the course Gitlab, towards the middle of the page you will see a bar that includes information on what branch you are on (will usually default to **master**), what project is called, the history, “find file” feature, and “web IDE”. Next to this feature is a graphic with an arrow pointing down, signifying that you can **download** the source code to your local computer. 

Once you click on the arrow, you will have the options to download the source code as a **zip, tar.gz, tar.bz2, and tar** file. It is recommended that you download the file as a **zip**, as it is normally the most supported type of file on computers, with an easy unzip feature to look at all of the information. 

Once the download is complete, it will download the master branch source code to your local hardware, in which you can place into any folder or location that you deem necessary. **NOTE** that you will not be able to make pushes or utilize git after downloading this project, as simply downloading the project places it onto your computer and does not give access to the work itself. 

### Utilizing Git
Next to the download option is a blue button that says **Clone**. This feature has multiple options as well, being **Clone with SSH**  and  **Clone with HTTP**. The difference between these options is in the protocol that is used when cloning the repository to local hardware.

SSH has the advantage that you can use public key authentication, while you must use a username and password when cloning through HTTPS. HTTPS offers the advantage that it tends to fare nicer with firewalls as opposed to SSH. Both of these options get the repository onto your computer and allow you to interact with remotes in the same way. 

In order to clone the code onto your local computer, go into the terminal or command prompt, and type in **git clone**, followed by whichever link that you copy, whether it be the **SSH** or **HTTPS** link. Once this step is complete, the repository will be placed onto your local computer, and will allow you to interact with the program in order to make pushes, commits, etc.

## * How to Run the Product
This section will describe how to use the product PliroMe. This product is very simple to use, and has very easy features to follow and buttons to choose that allow the human computer interaction to be seamless. 

### Running the Product
After downloading the project to your local repository, first you will need to make sure that you have all of the proper Python packages installed. The Python packages that will need to be installed are as follows:
- Flask (Flask, request, render_template, redirect, url_for, session)
- Json
- Pyrebase

You can view the following documentations for all of these, as well as the documentation for Firebase at:
- [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
- [Json Documentation](https://docs.python.org/3/library/json.html)
- [Pyrebase Documentation](https://github.com/thisbejim/Pyrebase)
- [Firebase Documentation](https://firebase.google.com/docs)

Once these packages are completely run, you will ideally need to run a virtual environment in python in order to run the website. In order to install, follow the directions below (**Note**: Make sure to insert this command in the main project directory file): 

Creating a Virtual Environment on macOS and Linux:
- ‘python3 -m venv env’ (can replace ‘env’ with whatever name you want)

Creating a Virtual Environment on Windows:
- ‘py -m venv env’ 

Once installation is complete, you will need to activate the virtual environment. In order to do this, follow the directions below:

Activating a Virtual Environment on macOS and Linux:
- ‘source env/bin/activate’ (or whatever you named ‘env’)

Activating a Virtual Environment on Windows:
- ‘.\env\Scripts\activate’

Now that the virtual environment is running (You can confirm this by checking the left side of the command line, it should say (env) on the side), you will need to install the packages included in ‘requirements.txt’. In order to do this, you will need to download the requirements.txt file, and then type:
- ‘pip install -r requirements.txt’

After the proper packages inside of the requirements.txt file installs, it is now time to run the website. To do this, move to the ‘course_project’ file (**‘cd course_project’**), and then run:
- ‘flask run’

This command will start up, and then provide you a link to click or copy + paste in your browser in order to access the application. Once you start the website, you will be able to sign up for an account, login with your information, and complete all the functionality described (check profile, create groups, create payments, etc). Our group created an easy-to-follow user interface to allow users to deploy the website and immediately benefit from all of it's functions without a large learning curve. 

## * How to Run Tests for this Product
The CI/CD calls so that our project will automatically run the tests, and then print a coverage report for the project. In order to run the tests manually if you would like, please do the following: 
- python -m pytest
- pytest --cov=course_project/ tests

## * Using the Product
Once you successfully launch the system, you will be met with a login page, welcoming you to PliroMe's website. If you already have an account, log in to the website using your email and password associated with your account. Otherwise, you will need to click on the **sign up** and enter the information it asks for, including your name, email, venmo, username, and password. Once this is done and you click on the **sign up** button to confirm, you will be redirected to the login screen to attempt to log in again. There is the option for the website to **remember me**, meaning that it will save your accounts information and attempt to log in with those credentials automatically when launching the website.

After logging in to the wesbite, PliroMe will redirect you to your **home** page, displaying the current groups that you are in, a tutorial video, a profile picture that you can change whenever you want, the option to create a new group, and a bar of options that you can click from anywhere on website, including a "My Balance" tab, "Settings" tab, and "Log Out" tab. The display bar at the top of the page is responsible for the following:
- Clicking on your **username** will return you to the main home page 
- Clicking on **My Balance** will redirect you to a page that displays the current balance that you have tracked in the application from all of the purchases that you have been associated with. If your balance is 0, the number will appear as black. If your balance is below 0, the number will appear as red. If your balance is above 0, the number will appear as green
- Clicking on the **Settings** button will redirect you to the Settings page that PliroMe has. There, you will be able to connect your Venmo account to the application and delete your account if you want to
- Clicking on the **Log Out** button will log the current user out of the system, and redirect the user to the **login** page again

If you are currently in a group, it will appear as one of the dropdown options on the home page. Once selecting the group that you want, you can click on **Go To Group** and it will take you to that specific group's page. If you have not become a member of a group, you can click on the **+** button in order to create a group. This form will ask you for the group's name, as well as who you want to add to that group. You can type in specific members that you want to add, or hold (CTRL on Windows, CMD on Mac) and select multiple members from the menu provided.

After being redirected to a specific group's page, you will be displayed information about the **group members** and the **purchases made** within this group, as well as a button that will allow you to see who owes who money within the specific group. You will also see a profile picture for that group that you can change whenever you want. Inside of the **purchases** section, there will be information on the specific item, buyer, and price. An image of a receipt or confirmation of payment can also be uploaded, which will appear under the list of purchases.

To create a new purchase, scroll down until you see the **Add Purchase** option. Once clicking on this button, you will be redirected to a page that will ask for the item name, price, and percentage of the payment distribution. The user can add any percentage to a specific member for how much they have to pay, but it is paramount to remember that **The total percentage for the payment needs to add up to 100%**. You then have the option to upload an image of your receipt/confirmation of purchase. Once you click **browse**, locate the image and confirm that you want to use it. It will refresh the page slightly, but **will not say anything in the bar that it has been submitted**. **DO NOT WORRY**, your image was submitted successfully.

To view a list of transactions that need to made for the specific group, scroll down until you see the **Get Transaction List** button. After clicking this button, you will be redirected to a new page that will show a list with the format: "Person A owes Person B $X". You can click the "Send Venmo Requests" button in order to make the requests through your account based on the transaction list. You can also click on "leave group" at the bottom of the page in order to have your user leave that current group that you are in, and you can also delete individual purchases that are made within the group.

## 1. Introduction
Managing group payments does not seem like a difficult task for the average human to perform, but participation in multiple, large groups with countless bills and payments can turn out to be one of the biggest headaches for anyone to have to deal with. In this proposal, we introduce “PliroMe”, a system whose purpose is to streamline this process and make it an ease for all parties involved within these complex payments. 

Currently, there are few mobile applications available that can split transfers between groups. The lacking feature shared between these applications is that they do not have ways to make transactions directly through the application, meaning an email or notification will be sent to the user as to how much they owe to the respective member. Because of this, most groups must resort to the manual division of the paychecks, usually having a single person pay for the entire bill and then charge their friends individually through Venmo or other payment applications. This often becomes an inconvenience for all parties involved: the person to charge may not request the proper amount of money from each person, the people to pay may not pay the proper amount on time or even at all, the overwhelming amount of bills may get confusing and have people lose track, and many more. 

Being a group of college students building this application, many of the product developers can attest to the fact that keeping track of bills is extremely overwhelming, and it takes a lot of meticulous work in order to get the proper amount of money paid back to you once you complete a purchase. Especially living in a house in a college town, one person is usually responsible for keeping accounts for each person paying for the water bill, electricity bill, furniture, groceries, hygiene supplies, and more. Furthermore, having to make payments and make sure people are paying you back is even more difficult during the school semester and more so during the COVID-19 pandemic, when the demand for money has been even tighter than ever. 

With these problems in mind, our group has decided to propose PliroMe, a system that will manage payment splitting while also having the ability to connect to payment applications in order to create transactions from the application directly, making sure that you receive your money on time and appropriately. 

## 1.1 Goals
The main goal of this project is to build PliroMe, a system for tracking payment splitting between large groups of people and minimizing the amount of manual work that users need to do to manage their money. PliroMe will do this by offering an easy-to-use interface that students, housemates, friends, vacation groups, and more can use to submit, create transactions, and track the amount of money that they owe to a specific person and how much money is owed to them by what specific user. 

## 1.2 Target Audience
The PliroMe team envisions that this system can be used by all people involved with group payments. This can range from vacation groups to housemates to friends going out to eat. Since splitting bills between people is a problem that causes a lot of hassle for all parties involved, the team did their best to ensure that all stakeholders in the process of payment splitting are positively benefited by the solution that they proposed. 

First and foremost, users will not have to manually keep track of all the different groups that they are involved in and the payments that are made within these groups. People go out with different groups to eat, buy groceries, buy furniture, and more, so having to manage all of the splitting of these bills is at best infeasible and at worst, impossible. The PliroMe system will alleviate much of this stress by giving users a place to go where all of their groups and bills are stored for them. In addition to submitting bills and making groups, the user will also be able to look at their main profile picture, finding a page that shows them how much money they are owed, and by which users they are owed money by. Additionally, it will also display how much money that the user owes to other people, and the specific amount associated. Overall, we believe that PliroMe will greatly help users deal with the annoying issue of splitting payments among groups of people in a way that makes the process very easy and ultimately allows them to spend less time on managing these tasks. 

In addition to the simple payment tracking between groups of friends and members of a house of organization, PliroMe will also be enjoyed by groups that are going on vacation or a group trip. Keeping track of all the multiple payments that are made throughout the trip is difficult, and coming home exhausted to long receipts to try to split is a headache that users often do not want to deal with. With the implementation of Venmo in PliroMe, the user will be able to simply input the members of their group, how much the total cost was, and send requests to all the other users of the group in order to get paid back for whatever activities that they had during the day. 

Finally, another example of an audience that will find great use of our application are large companies that are managing money between different financial sectors or sub-teams within the organization. Within large companies, enormous budgets are often divided amongst sectors within the company to spend on development, products, and other things to help benefit and better that specific sector. Because of this, keeping track of payments can become complicated and difficult to deal with. PliroMe would make this process seamless, as it would all be included in the single app that the heads of each sector can check into to see how much money they are expected to pay back to the head of the company in order to make sure that they did not spend too much out of the budget. 

## Developer Documentation
Our product, PliroMe, splits the cost of expenses in a group between numerous users and methods of cost splitting.  The team is using firebase as a way to develop our web application and structure our database.  PliroMe is similar to and will use the application Venmo which also uses firebase.  

Firebase provided build features:
- Authentication
- Firestore Database
- Realtime Database
- Storage
- Functions

The authentication feature in Firebase allows us to keep track of the exact users that register with the sign up page on our website. Once they input their information, the authentication page will contain the identifier (email), the date of creation, the date that they signed in, and an unique user ID for identification. 

Our realtime database is used to store the users that have made accounts on our application as well as the groups they are a part of.  A user contains their email, name, venmo, username, and groups they are a part of.  A group has a unique name and contains multiple members and their purchases.

### Project Structure
Our project utilizes Flask, Python, and HTML in order to create a working website that interacts with the Firebase data system in order to keep information of users of our application. Our project is built on the foundation of three files, 'group.py', 'person.py', and 'purchase.py'.

 These three files contains classes (named appropriately) that serve the purpose of facilitating adding and retrieving information from the Firebase database. When someone signs up with PliroMe, the 'Person' class is used in order to add the user to the Firebase database itself, under the database child 'users'. After they are in our system, they can then create groups (which is initiliazed with 'group.py') and also create purchases for those individual groups (complete with 'purchase.py'). 

In order to connect to the database itself, 'firebase_config.py' utilizes the 'pyrebase' package within Python, and API that allows us to easily connect with the database. After completing the configuration, we can then initialize the connection to Firebase and proceed with our functions inside of 'login_system.py', which allow the user to sign up, log in, and log out of their account. 

Finally, we can expose our application to the web utilizing Flask and HTML, which you can see in the 'templates' folder and 'app.py' file. These HTML templates, powered by the Flask functionality allow the user to see different pages, input text, and choose buttons in order to navigate through our system. 

### Sphinx Developer Documentation
Our project has Sphinx documentation that generates automatically. This Sphinx documentation is useful for developers who intend to learn the code and use it for their own purposes. To generate the Sphinx documentation, the developer must change directory into the docs folder. Assuming you start in the course-project folder.

cd docs

make.bat html

Running make.bat html will generate the html sphinx documentation in the build/html folder. If you open the file titled 'index.html' in your browser, you can navigate between different classes and view the documentation for the classes and their functions. 

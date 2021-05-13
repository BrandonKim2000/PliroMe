import pyrebase

"""This file is responsible for initializing the Firebase system with our application so that the two can work
seamlessly in tandem. The firebaseConfig file includes many dictionary key-value pairs, including the apiKey and
authDomain."""

firebaseConfig = {
    'apiKey': "AIzaSyDnZlxJHuFs2rm-YRjHYHATMoOF2uj6Dwg",
    'authDomain': "plirome.firebaseapp.com",
    'databaseURL': "https://plirome-default-rtdb.firebaseio.com",
    'projectId': "plirome",
    'storageBucket': "plirome.appspot.com",
    'messagingSenderId': "1054854821310",
    'appId': "1:1054854821310:web:010536386fe99966a4f5ef",
    'measurementId': "G-23X6XL9KWR"
}

py_firebase = pyrebase.initialize_app(firebaseConfig)
storage = py_firebase.storage()

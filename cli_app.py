import mysql.connector as mcon
import requests as re
import json
import sys


class DroneBaseUser():

    # CONSTRUCTOR THAT INITIALISES THE DATABASE INSTANCE AND CONNECTS TO REMOTE MYSQL DATABASE SERVER
    def __init__(self):
        self.db = mcon.connect(
            database="sql6479048",
            host="sql6.freemysqlhosting.net",
            user="sql6479048",
            password="CCrB4L9Q4R",
            port=3306
        )
        self.cur = self.db.cursor()
        self.permit = False

    # DELETES SPECIFIED USER
    def delete(self, user):
        try:
            self.cur.execute(f"delete from USERS where USERNAME='{user}' ;")
            return True
        except:
            print("User you want to delete does not exists")
            return False

    # FOR CREATION OF NEW USER
    def create(self, user, password):
        try:
            a = 'insert into USERS(USERNAME,PASSWORD) values (%s,%s)'
            b = (user, password)
            self.cur.execute(a, b)
            self.db.commit()
            return True
        except:
            print(f"User:'{user}' can not be created")
            return False

    # DISPLAYS ALL THE USERNAMES
    def display(self):
        try:
            self.cur.execute("select USERNAME from USERS;")
            for x in self.cur:
                print(x[0])
            return True
        except:
            print("Something went wrong, Can not fetch user data!")
            return False

    # UPDATES USERNAME / PASSWORD BASED ON ADMIN REQUIREMENTS
    def update(self, user):
        print("What do you want to update?\n1.Username\n2.Password\n :")
        n = int(input())
        if n == 1:
            username = input("Enter your new Username: ")
            self.cur.execute(f"update USERS set USERNAME = '{username}' where USERNAME='{user}' ")
            self.db.commit()
            print(f"Username updated from '{user}' to '{username}' successfully!")
            return True
        elif n == 2:
            password = input("Enter your new Password: ")
            self.cur.execute(f"update USERS set PASSWORD='{password}' where USERNAME='{user}'")
            self.db.commit()
            print(f"Password updated for '{user}' successfully!")
            return False
        else:
            print("You have entered wrong value!")
            return False

    # USER LOGS IN , TO ACCESS ALL THE SERVICES
    def login(self, user, password):
        try:
            self.cur.execute(f"select * from USERS where USERNAME='{user}' and PASSWORD='{password}'")
            if len(self.cur.fetchall()) >= 1:
                print(f"{user} Logged in successfully!")
                return True
            else:
                print(f"Not recognised! Please try again!")
                return False
        except:
            print("Something went wrong! Please check your internet connection!")
            return False

    # USER LOGS OUT OF THE PORTAL
    def logout(self):
        self.permit = False

    # GETS INFORMATION ABOUT THE WEATHER BASED ON LONGITUDE AND LATITUDE VALUES
    def getinfo(self, lat, lon):
        try:
            x = re.get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=33d040191e3b597424e483acb5b7f948")
            resp = (x.text)
            d = json.loads(resp)
            print("Following info has been fetched:")
            print(
                f"1.Humidity: {d['main']['humidity']}\n2.Pressure: {d['main']['pressure']}\n3.Average temperature: {d['main']['temp']}\n4.Wind Speed: {d['wind']['speed']}\n5.Wind degree: {d['wind']['deg']} \n6.Visibility: {d['visibility']}\n")
        except:
            print("You might have entered wrong values of Longitude/ Latitude OR Please Check you Internet Connection")


# Program starts from here - > as soon as we run the CLI new object is created from class DroneBaseUser

if sys.argv[1] == "--h" or sys.argv[1] == "--help" or sys.argv[1] == "--H":
    print("----------This is a CLI App from DroneBase------------\n")
    print("If User already has an account, then they must Login: 1")
    print("If user does not have an account, Please Sign in with: 2")
    print("After Successfully Logging into the CLI Portal:")
    print("Use: 1 to Create a new user to the Database")
    print("Use: 2 to Delete pre-existing user account")
    print("Use: 3 to Update User Information on Database")
    print("Use: 4 to Read All User Information")
    print("Use: 5 to See the Weather information")
    print("Use: 6 to Logout the already Logged In User")

ob = DroneBaseUser()
while (ob.permit == False):
    n = int(input("Select:\n 1. Login\n 2.Sign Up : "))
    if n == 1:
        print("Enter Username: \t")
        username = input()
        print("Enter Password: \t")
        password = input()
        ob.permit = ob.login(username, password)
        if ob.permit:
            print(f"Login Success for user: {username}")
        else:
            print(f"Looks like you've input wrong username or password, {username}!")
    else:
        username = input("Enter your preferred Username: ")
        password = input("Enter your password: ")
        ob.permit = ob.create(username, password)
        if ob.permit:
            print(f"User {username} has been created successfully")

c = 'y'
while (c == 'y' or c == 'Y'):
    n = int(input(
        "\n1. Create User\n2. Delete User\n3. Update User\n4. Read All Users\n5. Weather Information\n6. LogOut  :"))
    if (n == 1):
        x = False
        while (x != True):
            username = input("Enter New Username: ")
            password = input("Enter your Password: ")
            x = ob.create(username, password)
            if x == True:
                print(f"User {username} created Successfully !")
            else:
                print(f"User with username: {username} already exists.")
    elif n == 2:
        x = False
        while (x != True):
            username = input("Enter username you want to delete: ")
            x = ob.delete(username)
            if x == True:
                print(f"User {username} Deleted Successfully !")
                break

    elif n == 3:
        x = False
        while (x != True):
            username = input("Enter  Username you want to Update: ")
            password = input("Enter the password: ")
            x = ob.update(username)

    elif n == 4:
        ob.display()


    elif n == 5:
        lat = input("Enter the Latitude Value/Location: ")
        long = input("Enter the Longitude Value/Location: ")
        ob.getinfo(lat, long)

    elif n == 6:
        ob.logout()
        print("User Logged out Successfully")
        break

    else:
        print("Please Enter a Valid Choice(1-5)")

    c = input("\nDo you want to continue (y/Y) ")

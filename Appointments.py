# This class will include details of all visitors/user
# Before scheduling appointment user need to create his/her own profile

import User
import pymongo

#insert new user
def insertNewUser(user_name,passport,email,password):
        connection_string = "mongodb+srv://dbUser:Qwepoi.123@cluster0.bzlp2.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
        my_client = pymongo.MongoClient(connection_string)
        db = my_client["Vaccine_Finder"]
        vaccine = db["Certificate"]
        mydict = {"user_name": user_name, "passport": passport, "email": email, "password": password}
        vaccine.insert_one(mydict)
        return True


# validate registration
def vaidateRegistrarion():
    pass

# Method will create user profile based on info from client side
def intiate_appointment():
    pass

# Method will update existing appointment
def update_appointment():
    pass


# Method will retrieve all appointments from Database based on unique id
def get_appointment_details_byId():
    pass


# Method to retrieve all appointments
def get_all_appointment_details():
    pass




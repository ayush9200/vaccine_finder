# This class will include details of all visitors/user
# Before scheduling appointment user need to create his/her own profile

import User
import pymongo
from datetime import date
import datetime


#insert new user
def insertNewUser(user_name,passport,email,password):
        userAlreadyExists = userExistsCheck(user_name,passport)
        if userAlreadyExists:
            return False
        else:
            connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
            my_client = pymongo.MongoClient(connection_string)
            db = my_client["Vaccine_Finder"]
            vaccine = db["Appointments"]
            newUser = {"user_name": user_name, "passport": passport, "email": email, "password": password,"bookingDate":"0000-00-00","vaccinationCompleted":False}
            vaccine.insert_one(newUser)
            return True
        return False


# validate User already exists
def userExistsCheck(user_name, passport):
    connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)
    db = my_client["Vaccine_Finder"]
    mycol = db["Appointments"]
    clms = {"user_name","passport"}
    result = mycol.find_one({'$and' : [{'user_name':user_name}, {'passport':passport}]},clms)
    if result is None:
        print("No such user exists. Registration can be done.")
        return False
    else:
        print("User already exists. Registration cannot be done.")
        for x in result:
            print(x)
        return True
    return False


# validate registration
def vaidateRegistrarion(user_name, passport, password):
    connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)
    db = my_client["Vaccine_Finder"]
    mycol = db["Appointments"]
    clms = {"user_name","passport","password"}
    result = mycol.find_one({'$and' : [{'user_name':user_name}, {'passport':passport}, {'password':password}]},clms)
    if result is None:
        return False
    else:
        for x in result:
            print(x)
            return True
    return False



# validate Booking
def vaidateBooking(user_name, passport, password):
    connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)
    db = my_client["Vaccine_Finder"]
    mycol = db["Appointments"]
    clms = {"bookingDate"}
    result = mycol.find({'$and' : [{'user_name':user_name}, {'passport':passport}, {'password':password}]})
    print("In validate booking")
    if result is None:
        return False
    else:
        for x in result:
            print(x.get('bookingDate'))
            if x.get('bookingDate') == "0000-00-00":
                return True
    return False


# Method will get the date of an already booked item, this will be further used to diaplay result
def getAlreadyBookedDate(user_name, passport,email):
    connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)
    db = my_client["Vaccine_Finder"]
    mycol = db["Appointments"]
    clms = {"bookingDate"}
    result = mycol.find({'$and': [{'user_name': user_name}, {'passport': passport}, {'email': email}]})
    print("In get already booked date")
    if result is None:
        return False
    else:
        for x in result:
            print(x.get('bookingDate'))
    return x.get('bookingDate')

# Method will update existing appointment
def update_appointment():
    pass


# Method will retrieve all appointments from Database based on unique id
def validate_appointment_date(bookingDate):
    splt = bookingDate.split("-", 3)
    # print(splt[0])
    # print(splt[1])
    # print(splt[2])
    bookingDate = datetime.date(int(splt[0]), int(splt[1]), int(splt[2]))
    print(bookingDate)
    today = date.today()
    print("Today's date:", today)
    if bookingDate > today:
        print("Date is correct")
        return True
    else:
        return False


# Method to finally update appointment in database
def bookAppointment(user_name,passport,email,booking_date,book_location):
    print("in update boking")
    connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)
    db = my_client["Vaccine_Finder"]
    vaccine = db["Appointments"]
    myquery = {"user_name": user_name, "passport": passport, "email": email}
    newvalues = {"$set": {"bookingDate": booking_date}}
    vaccine.update_one(myquery, newvalues)

    vaccineLocation = db["VaccineLocations"]
    clms = {"vaccinesLeft"}
    result = vaccineLocation.find({"locationName": book_location})
    print("In update location booking")
    for x in result:
        vaccinesLeft = x.get('vaccinesLeft')
    updatevaccinesLeft = int(vaccinesLeft - 1)
    myquery = {"locationName": book_location}
    newvalues = {"$set": {"vaccinesLeft": int(updatevaccinesLeft)}}
    vaccineLocation.update_one(myquery, newvalues)




import pymongo
from datetime import date
import datetime


#insert new user feedback
def insertNewFeedback(fName,lName,subject,pNum):
    connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)
    db = my_client["Vaccine_Finder"]
    feedback = db["Feedbacks"]
    newFeedback = {"fName": fName, "lName": lName, "pNum": pNum, "subject": subject}
    feedback.insert_one(newFeedback)
    return True
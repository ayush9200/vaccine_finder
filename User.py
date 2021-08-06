import pymongo


class User:

    '''
        _id:610c00097b5ece0075b55f67
        user_name:"Sami"
        passport:"XYZ"
        email:"sami@ggmail.com"
        password:"sami"
        bookingDate:"2021-08-27"
        vaccinationCompleted:true
    '''


    def getAllUserDetails(self):
        connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
        my_client = pymongo.MongoClient(connection_string)
        db = my_client["Vaccine_Finder"]
        appointment_collection = db["Appointments"]
        listOfUsers = appointment_collection.find()
        count = 1
        dataList = []
        for data in listOfUsers:
            userData = {}
            userData["count"] = count
            userData["name"] = data["user_name"]
            userData["bookingDate"] = data["bookingDate"]
            userData["passport"] = data["passport"]
            if data["vaccinationCompleted"]:
                userData["status"] = "Active"
            else:
                userData["status"] = "Inactive"
            userData["email"] = data["email"]
            dataList.append(userData)
            count += 1

        return dataList








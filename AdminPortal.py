import pymongo


class AdminPortal:

    def authenticate(self, username, password):
        connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
        my_client = pymongo.MongoClient(connection_string)
        db = my_client["Vaccine_Finder"]
        admin_cred = db["Admin"]
        results = admin_cred.find({"$and": [{"username": username}, {"pass": password}]})
        cred = False
        for row in results:
            cred = True
        return cred


    def getAppointmentStatus(self):
        connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
        my_client = pymongo.MongoClient(connection_string)
        db = my_client["Vaccine_Finder"]
        vaccine = db["Appointments"]
        results = vaccine.find()
        countForTotal = 0
        for row in results:
            countForTotal += 1
           # print(row)

        ongoing = countForTotal - 2
        upcoming = 2
        cancelled = 0
        total = countForTotal
        list_To_Return = [ongoing, upcoming, cancelled, total]
        return list_To_Return

    def getVaccinationStatus(self):
        connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
        my_client = pymongo.MongoClient(connection_string)
        db = my_client["Vaccine_Finder"]
        vaccine = db["Appointments"]
        available_vc = 240
        unused = 32
        expired = 8
        days = 2
        vaccination_status = [available_vc, unused, expired, days]
        return vaccination_status


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
            userData["status"] = data["vaccinationCompleted"]
            userData["email"] = data["email"]
            dataList.append(userData)
            count += 1

        return dataList

    def getAllNonVaccinatedUsers(self):
        connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
        my_client = pymongo.MongoClient(connection_string)
        db = my_client["Vaccine_Finder"]
        appointment_collection = db["Appointments"]
        listOfUsers = appointment_collection.find()
        count = 1
        dataList = []
        for data in listOfUsers:
            if not data["vaccinationCompleted"]:
                userData = {}
                userData["count"] = count
                userData["name"] = data["user_name"]
                userData["bookingDate"] = data["bookingDate"]
                userData["passport"] = data["passport"]
                dataList.append(userData)
                count += 1

        return dataList

    def markUserAsVaccinated(self, passportNo):
        try:
            connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
            my_client = pymongo.MongoClient(connection_string)
            db = my_client["Vaccine_Finder"]
            appointment_collection = db["Appointments"]
            whereClause = {"passport": passportNo}
            setValue = {"$set": {"vaccinationCompleted": True}}
            appointment_collection.update_one(whereClause, setValue)
            return True
        except:
            return False


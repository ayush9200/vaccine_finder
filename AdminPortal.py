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
            print(row)

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


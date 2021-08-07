import triggerEmail


class AdminPortal:

    def authenticate(self, username, password, my_client):
        db = my_client["Vaccine_Finder"]
        admin_cred = db["Admin"]
        results = admin_cred.find({"$and": [{"username": username}, {"pass": password}]})
        cred = False
        for row in results:
            cred = True
        return cred


    def getAppointmentStatus(self, my_client):
        db = my_client["Vaccine_Finder"]
        vaccine = db["Appointments"]
        results = vaccine.find()
        countForTotal = 0
        for row in results:
            countForTotal += 1

        ongoing = countForTotal - 2
        upcoming = 2
        cancelled = 0
        total = countForTotal
        list_To_Return = [ongoing, upcoming, cancelled, total]
        return list_To_Return

    def getVaccinationStatus(self, my_client):
        db = my_client["Vaccine_Finder"]
        vaccine = db["Appointments"]
        available_vc = 240
        unused = 32
        expired = 8
        days = 2
        vaccination_status = [available_vc, unused, expired, days]
        return vaccination_status


    def getAllUserDetails(self, my_client):
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

    def getAllNonVaccinatedUsers(self, my_client):
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

    def markUserAsVaccinated(self, passportNo, my_client):
        try:
            db = my_client["Vaccine_Finder"]
            appointment_collection = db["Appointments"]
            whereClause = {"passport": passportNo}
            setValue = {"$set": {"vaccinationCompleted": True}}
            appointment_collection.update_one(whereClause, setValue)
            self.fireEmailAfterUpdate(passportNo)
            return True
        except:
            return False

    def getVaccineStatusLocationWise(self, my_client):
        vaccineDataList = []
        try:
            db = my_client["Vaccine_Finder"]
            vaccine_collection = db["VaccineLocations"]
            listFromMongo = vaccine_collection.find()
            for data in listFromMongo:
                vaccineData = {"count": int(data["vaccinesLeft"]), "locationName": data["locationName"]}
                vaccineDataList.append(vaccineData)
        except:
            return False
        return vaccineDataList

    def fireEmailAfterUpdate(self, passportNo, my_client):
        try:
            db = my_client["Vaccine_Finder"]
            appointment_collection = db["Appointments"]
            results = appointment_collection.find({"passport": passportNo})
            emailId = results.get("email")
            subject = "Congratulations! You are now fully vaccinated. Please get your Vaccine Certificate from our " \
                      "website.\n Also please follow all mandatory rules that have been specially made for vaccinated " \
                      "citizens. "
            triggerEmail.send_email(emailId, subject)
        except:
            return False

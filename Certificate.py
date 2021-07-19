import pymongo

def userFind(user_name,passport,password):
    connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)



    db = my_client["Vaccine_Finder"]
    mycol = db["Appointments"]

    result = mycol.find_one({'$and': [{'user_name': user_name}, {'passport': passport},{'password': password}]})

    if result:
        print("User found in the database")
        return True

    else:
        print("THis user is not found in database")
        return False



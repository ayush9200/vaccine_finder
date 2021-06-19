# Ayush Kumar Singh (C0799530) flask
from flask import Flask, request, render_template
import pymongo
import Profile
import User
import Appointments
import Organisations

app = Flask(__name__)

def intiate_mongoDb_conn():
    connection_string = "mongodb+srv://admin:root@cluster0.0kinj.mongodb.net/sample_restaurants?retryWrites=true&w=majority"
    mongo_client = pymongo.MongoClient(connection_string)



@app.route("/home")
def index():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.run()
    intiate_mongoDb_conn()
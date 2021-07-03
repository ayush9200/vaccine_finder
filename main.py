
from flask import Flask, request, render_template
import pymongo
import Profile
import User
import Appointments
import Organisations
import AdminPortal


app = Flask(__name__)

def intiate_mongoDb_conn():
    connection_string = "mongodb+srv://admin:root@cluster0.0kinj.mongodb.net/sample_restaurants?retryWrites=true&w=majority"
    mongo_client = pymongo.MongoClient(connection_string)



@app.route("/")
def index():
    return render_template('homepage.html')


@app.route("/admin", methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'GET':
        return render_template('login-page.html')
    else:
        return render_template('homepage.html')


@app.route("/admin-login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user_name = request.form.get("username")
        password = request.form.get("password")
        admin = AdminPortal.AdminPortal()
        action = admin.authenticate(user_name, password)
        if action:
            return render_template('login-success.html', username=user_name.upper())
        else:
            return render_template('login-fail.html')
    else:
        return render_template('login-fail.html')


# Started by Dashmeet Kaur

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        return render_template('homepage.html')


@app.route("/register-login", methods=['GET', 'POST'])
def register_login():
    if request.method == 'POST' and request.form["btn"] == "Register":
        print("Register clicked")
        user_name = request.form.get("name")
        passport = request.form.get("passport")
        email = request.form.get("email")
        password = request.form.get("inputPassword")
        action = Appointments.insertNewUser(user_name,passport,email,password)
        if action:
            return render_template('login-success.html', username=user_name.upper())
        else:
            return render_template('user-already-exists.html')

    elif request.method == 'POST' and request.form["btn"] == "Sign In":
        print("Sign in clicked")
        user_name = request.form.get("name")
        passport = request.form.get("passport")
        email = request.form.get("email")
        password = request.form.get("inputPassword")
        action = Appointments.vaidateRegistrarion(user_name, passport, password)

        if action:
            return render_template('login-success.html', username=user_name.upper())
        else:
            return render_template('user-login-fail.html')



if __name__ == "__main__":
    app.run()
    intiate_mongoDb_conn()
from flask import Flask, request, render_template
import pymongo
import Profile
import User
import Appointments
import Organisations
import AdminPortal
from Certificate import userFind
from flask import Flask, session
import triggerEmail
import calendar
import contactUs

from User import User

app = Flask(__name__)


def intiate_mongoDb_conn():
    connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
    mongo_client = pymongo.MongoClient(connection_string)



# Started by Ayush
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
        appointment_list_status = admin.getAppointmentStatus()
        vaccination_status = admin.getVaccinationStatus()
        wholeUserData = admin.getAllUserDetails()
        pendingUserList = admin.getAllNonVaccinatedUsers()
        if action:
            return render_template('login-success.html', username=user_name.upper(),
                                   og_appointment=appointment_list_status[0],
                                   upg_appointment=appointment_list_status[1],
                                   cld_appointment=appointment_list_status[2],
                                   ttl_appointment=appointment_list_status[3], available_vc=vaccination_status[0],
                                   unused_vc=vaccination_status[1], expired_vc=vaccination_status[2],
                                   days_vc=vaccination_status[3], data=wholeUserData, pendingUserDataList=pendingUserList)
        else:
            return render_template('login-fail.html')
    else:
        return render_template('login-fail.html')


@app.route("/vaccination-update", methods=['GET', 'POST'])
def vaccinationUpdate():
    if request.method == 'POST':
        passportNo = request.form.get("passport")
        admin = AdminPortal.AdminPortal()
        updated = admin.markUserAsVaccinated(passportNo)
    return render_template('vaccination-update.html', updateStatus=updated);

# Ended by Ayush

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
        session['user_name'] = user_name
        passport = request.form.get("passport")
        session['passport'] = passport
        email = request.form.get("email")
        session['email'] = email
        password = request.form.get("inputPassword")
        session['password'] = password
        action = Appointments.insertNewUser(user_name, passport, email, password)
        if action:
            return render_template('login-success-book.html', username=user_name.upper())
        else:
            return render_template('user-already-exists.html')

    elif request.method == 'POST' and request.form["btn"] == "Sign In":
        print("Sign in clicked")
        user_name = request.form.get("name")
        session['user_name'] = user_name
        passport = request.form.get("passport")
        session['passport'] = passport
        email = request.form.get("email")
        session['email'] = email
        password = request.form.get("inputPassword")
        session['password'] = password
        action = Appointments.vaidateRegistrarion(user_name, passport, password)
        if action:
            action = Appointments.vaidateBooking(user_name, passport, password)
            if action:
                print("going to sign in")
                return render_template('login-success-book.html', username=user_name.upper())
            else:
                appointmentDate = Appointments.getAlreadyBookedDate(user_name, passport,email)
                print("Already booked date is " + appointmentDate)
                splt = appointmentDate.split("-", 3)
                yr = splt[0]
                date = splt[2]
                monthName = calendar.month_name[int(splt[1][1:])]
                return render_template('login-success-signin.html', username=user_name.upper(),
                                       appointmentDate = appointmentDate, year=yr, date=date, monthName=monthName)
        else:
            return render_template('user-login-fail.html')


@app.route("/book-my-apptmnt", methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        print("in book appointment clicked")
        booking_date = request.form.get("book-date")
        print(booking_date)
        book_location = request.form.get("book-location")
        print(book_location)
        user_name = session['user_name']
        passport = session['passport']
        email = session['email']
        password = session['password']
        validDate = Appointments.validate_appointment_date(booking_date)
        if validDate == True:
            Appointments.bookAppointment(user_name,passport,email,booking_date,book_location)
            triggerEmailObj = triggerEmail.TriggerEmail()
            triggerEmailObj.send_email("Appointment booked for " + user_name + " on " + booking_date + " at " + book_location,
                                       "Hello Dear \n" + user_name + "Your appointment for covid-19 vaccination" +
                                       " on date selected " + booking_date + " at " + book_location+ " is confirmed!\n\n" +
                                       "Put your mask on and stay safe.\nRegards,\n Lambton Covid-19 team", email)
            return render_template('booking-success.html', username=user_name.upper(), booking_date=booking_date,book_location=book_location)
    else:
        return render_template('login-fail.html')


@app.route("/cert", methods=['GET','POST'])
def Certificate():
    if request.method=='GET':
        return render_template('Certificate.html')
    else:
        return render_template('homepage.html')


@app.route("/get-certificate", methods=['GET','POST'])
def get_certificate():
    if request.method == 'POST' and request.form["btn"] == "Get Certificate":
        print("Get Certificate button clicked")
        user_name= request.form.get('name')
        passport = request.form.get('passport')
        password = request.form.get('inputPassword')
        action = userFind(user_name,passport,password)
        if action:
            return render_template('certificate-found.html',username=user_name.upper() )
        else:
            return render_template('user-login-fail.html')

#
# @app.route('/about')
# def about_us():
#     return render_template('FAQ.html')


@app.route("/faq", methods=['GET','POST'])
def about_us():
    if request.method=='GET':
        return render_template('FAQ.html')
    else:
        return render_template('homepage.html')

@app.route("/contactUs", methods=['GET','POST'])
def contact_us():
    if request.method=='GET':
        return render_template('contact_us.html')
    else:
        return render_template('homepage.html')

@app.route("/contactFormSubmitted", methods=['GET','POST'])
def contactFormSubmitted():
    if request.method == 'POST':
        print("Contact us form submitted")
        firstname= request.form.get('firstname')
        lastname = request.form.get('lastname')
        subject = request.form.get('subject')
        phoneNum = request.form.get('phonenumber')
        action = contactUs.insertNewFeedback(firstname,lastname,subject,phoneNum)
        if action:
            return render_template('thanksForFeedback.html',username=firstname.upper())
        else:
             return render_template('user-login-fail.html')



if __name__ == "__main__":
    app.config['SECRET_KEY'] = "abcd"
    app.run()
    intiate_mongoDb_conn()
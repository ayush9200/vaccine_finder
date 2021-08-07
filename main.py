from flask import Flask, request, render_template
import pymongo
import Appointments
import AdminPortal
from Certificate import userFind
from flask import Flask, session
import triggerEmail
import calendar
import logging
import contactUs

# Starting application
app = Flask(__name__)


# Started by Ayush

logger = logging.getLogger()
# Create logger handlers for both file and console
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('server.log')

# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - VaccineFinder - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - VaccineFinder - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)    # Handler for writing logs in console
f_handler.setFormatter(f_format)    # Handler for writing logs in file
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.setLevel(logging.INFO)       # Setting logger level at info


@app.route("/")
def index():
    logger.info('Redirecting to homepage')
    return render_template('homepage.html')


@app.route("/admin", methods=['GET', 'POST'])
def admin_panel():
    logger.info('Redirecting to Admin Panel')
    if request.method == 'GET':
        return render_template('login-page.html')
    else:
        return render_template('homepage.html')


@app.route("/admin-login", methods=['GET', 'POST'])
def admin_login():
    logger.info('Redirecting to Admin Login Panel')
    connection_string = "mongodb+srv://dbUser:dbUser@cluster0.w78tt.mongodb.net/Vaccine_Finder?retryWrites=true&w=majority"
    my_client = pymongo.MongoClient(connection_string)
    if request.method == 'POST':
        user_name = request.form.get("username")
        password = request.form.get("password")
        admin = AdminPortal.AdminPortal()
        logger.info('Admin authentication started')
        action = admin.authenticate(user_name, password, my_client)

        logger.info('Get Appointment Status')
        appointment_list_status = admin.getAppointmentStatus(my_client)

        logger.info('Get overall Vaccination Status')
        vaccination_status = admin.getVaccinationStatus(my_client)

        logger.info('Get user details for Admin')
        wholeUserData = admin.getAllUserDetails(my_client)

        logger.info('Get all non vaccinated users')
        pendingUserList = admin.getAllNonVaccinatedUsers(my_client)

        logger.info('Get Vaccine availability based on locations')
        vaccineLocationWiseData = admin.getVaccineStatusLocationWise(my_client)
        if action:
            return render_template('login-success.html', username=user_name.upper(),
                                   og_appointment=appointment_list_status[0],
                                   upg_appointment=appointment_list_status[1],
                                   cld_appointment=appointment_list_status[2],
                                   ttl_appointment=appointment_list_status[3], available_vc=vaccination_status[0],
                                   unused_vc=vaccination_status[1], expired_vc=vaccination_status[2],
                                   days_vc=vaccination_status[3], data=wholeUserData,
                                   pendingUserDataList=pendingUserList, vaccineData=vaccineLocationWiseData)
        else:
            logger.warning('Bad Credentials. Admin Login attempt failed')
            return render_template('login-fail.html')
    else:
        logger.warning('Bad Credentials. Admin Login attempt failed')
        return render_template('login-fail.html')


@app.route("/vaccination-update", methods=['GET', 'POST'])
def vaccinationUpdate():
    logger.info('Redirecting to Vaccination alert page')
    if request.method == 'POST':
        passportNo = request.form.get("passport")
        admin = AdminPortal.AdminPortal()
        updated = admin.markUserAsVaccinated(passportNo)
    return render_template('vaccination-update.html', updateStatus=updated);

# Ended by Ayush

# Started by Dashmeet Kaur


@app.route("/register", methods=['GET', 'POST'])
def register():
    logger.info('Redirecting to Register page')
    if request.method == 'GET':
        return render_template('register.html')
    else:
        return render_template('homepage.html')


@app.route("/register-login", methods=['GET', 'POST'])
def register_login():
    logger.info('Redirecting to Registration/Sign Login Panel')
    if request.method == 'POST' and request.form["btn"] == "Register":
        logger.info("Register clicked")
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
            logger.warning('Registration not completed. User already exist')
            return render_template('user-already-exists.html')

    elif request.method == 'POST' and request.form["btn"] == "Sign In":
        logger.info("Sign in clicked")
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
                logger.info("going to sign in")
                return render_template('login-success-book.html', username=user_name.upper())
            else:
                appointmentDate = Appointments.getAlreadyBookedDate(user_name, passport,email)
                logger.info("Already booked date is " + appointmentDate)
                splt = appointmentDate.split("-", 3)
                yr = splt[0]
                date = splt[2]
                monthName = calendar.month_name[int(splt[1][1:])]
                return render_template('login-success-signin.html', username=user_name.upper(),
                                       appointmentDate = appointmentDate, year=yr, date=date, monthName=monthName)
        else:
            logger.warning('User login failed')
            return render_template('user-login-fail.html')


@app.route("/book-my-apptmnt", methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        logger.info("Booking Appointment clicked")
        booking_date = request.form.get("book-date")
        book_location = request.form.get("book-location")
        user_name = session['user_name']
        passport = session['passport']
        email = session['email']
        password = session['password']
        validDate = Appointments.validate_appointment_date(booking_date)
        if validDate == True:
            logger.warning('Sending mail to : '+ email)
            Appointments.bookAppointment(user_name,passport,email,booking_date,book_location)
            triggerEmailObj = triggerEmail.TriggerEmail()
            triggerEmailObj.send_email("Appointment booked for " + user_name + " on " + booking_date + " at " + book_location,
                                       "Hello Dear \n" + user_name + "Your appointment for covid-19 vaccination" +
                                       " on date selected " + booking_date + " at " + book_location+ " is confirmed!\n\n" +
                                       "Put your mask on and stay safe.\nRegards,\n Lambton Covid-19 team", email)
            return render_template('booking-success.html', username=user_name.upper(), booking_date=booking_date,book_location=book_location)
    else:
        logger.warning('Login attempt failed')
        return render_template('login-fail.html')


@app.route("/cert", methods=['GET','POST'])
def Certificate():
    logger.info("Redirecting to Certificate page")
    if request.method=='GET':
        return render_template('Certificate.html')
    else:
        return render_template('homepage.html')


@app.route("/get-certificate", methods=['GET','POST'])
def get_certificate():
    if request.method == 'POST' and request.form["btn"] == "Get Certificate":
        logger.info("Get Certificate button clicked")
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
    logger.info("Redirecting to FAQ page")
    if request.method=='GET':
        return render_template('FAQ.html')
    else:
        return render_template('homepage.html')

@app.route("/contactUs", methods=['GET','POST'])
def contact_us():
    logger.info("Redirecting to Contact Us")
    if request.method=='GET':
        return render_template('contact_us.html')
    else:
        return render_template('homepage.html')

@app.route("/contactFormSubmitted", methods=['GET','POST'])
def contactFormSubmitted():
    logger.info("Redirecting to Contact Form")
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
from flask import Flask,request,render_template,redirect,flash,jsonify,session
import mysql.connector
import os
import re
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db import get_db_connection, init_db
from register import Registration
from signin import Signin
from trustregister import TrustRegistration

load_dotenv()
app = Flask(__name__)

# Ensure the database connection is established before handling requests
with app.app_context():
    init_db()

app.secret_key = 'jojo'
reg = Registration()
sig = Signin()
trus = TrustRegistration()

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', user=session.get('user'))

@app.route('/about')
def about():
    return render_template('about.html', user=session.get('user'))

@app.route('/contact')
def contact():
    return render_template('contact.html', user=session.get('user'))

@app.route('/signin', methods=['GET','post'])
def signin():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        
        is_signedin, message = sig.check_signin(user_email, user_password)
        if not is_signedin:
            flash(message)
            return redirect('/signin')
        
        else:
            user_data = sig.get_user_data_by_email(user_email)
            session['user'] = {
                'name': user_data["username"],
                'profile_pic': user_data.get('profile_pic', '/static/default.png'),
                'type': user_data.get('type')
            }
            return redirect('/')

        
    return render_template('signin.html')

#for user
@app.route('/register/user', methods=['GET','POST'], endpoint="register_user")
def register():
  
    if request.method == 'POST':
        username = request.form['login-name']
        userphone = request.form['login-phone']
        email = request.form['login-email']
        password = request.form['login-password']

        name = request.form.get('login-name')
        if not name or not re.match(r"^[A-Za-z\s]+$", name):
            flash("Invalid name format. Please use letters and spaces only.")
            return redirect('/register/user')

        is_valid, message = reg.validate_input(email, password)
        if not is_valid:
            flash(message)
            return redirect('/register/user')
    
        is_registered, message = reg.register_user(username, email, password, userphone)
        if is_registered:
            flash(message)
            return redirect('/signin')
        else:
            flash(message)
            return redirect('/register/user')
    
    return render_template('register.html', active_side='user')

#for trust
@app.route('/register/trust', methods=['GET', 'POST'])
def register_trust(): 

    if request.method == 'POST':   
        organisation_name = request.form['signup-organization-name']
        organisation_type = request.form['signup-organization-type']
        tax_identification_number = request.form['signup-tax-id']
        contact_person_name = request.form['signup-contact-name']
        contact_person_email = request.form['signup-contact-email']
        phone = request.form['signup-contact-phone']
        address = request.form['signup-address']
        password = request.form['signup-password']

        is_valid1, message = trus.validate_trust(contact_person_email, password)
        if not is_valid1:
            flash(message)
            return redirect('/register/trust')
    
        is_registered1, message = trus.register_trust(organisation_name, organisation_type, tax_identification_number, contact_person_name, contact_person_email, phone, address, password)
        if is_registered1:
            flash(message)
            return redirect('/signin')
        else:
            flash(message)
            return redirect('/register/trust')
    
    return render_template('register.html', active_side='trust')


@app.route('/current_user')
def current_user():
    return jsonify(session.get('user', {}))

# removes user from session

@app.route('/logout')
def logout():
    session.pop('user', None)  
    return redirect('/')


@app.route('/user')
def user():
    if 'user' not in session:
        return redirect('/signin')
    return render_template('user.html', user=session.get('user'))

@app.route('/donate', methods=['POST'])
def donate():
    donor_name = request.form.get('name')
    donor_phone = request.form.get('phone')
    donor_address = request.form.get('address')
    donor_landmark = request.form.get('landmark')
    donor_category = request.form.get('category')
    donor_description = request.form.get('description')

    # Fetch all registered trust emails
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT contact_person_email FROM trusts")
    trusts_email = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    # Send emails to all trusts
    failed_emails = send_emails_bulk(donor_name, donor_phone, donor_address, donor_landmark,
                                     donor_category, donor_description, trusts_email)

    if failed_emails:
        flash(f"Some emails failed to send: {', '.join(failed_emails)}")
    else:
        flash("Your donation info has been sent to all trusts successfully!")

    return redirect('/user')


def send_emails_bulk(donor_name, donor_phone, donor_address, donor_landmark,
                     donor_category, donor_description, email_list):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    subject = f"New Donation Request from {donor_name}"
    body = f"""
Donor Name: {donor_name}
Donor Phone: {donor_phone}
Item Category: {donor_category}
Item Description: {donor_description}
Address: {donor_address}
Landmark: {donor_landmark}
"""

    failed = []

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for email in email_list:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            try:
                server.send_message(msg)
            except Exception as e:
                print(f"Failed to send email to {email}: {e}")
                failed.append(email)

        server.quit()
    except Exception as e:
        print(f"SMTP connection failed: {e}")
        failed.extend(email_list)

    return failed

@app.route('/pickup')
def pickup():
    if 'user' not in session:
        return redirect ('/signin')
    return render_template('pickup.html', user=session.get('user'))

@app.route('/trust')
def trust():
    if 'user' not in session:
        return redirect('/signin')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("select organisation_name as trust_name, address, contact_person_name, contact_person_email from trusts")
        trusts_data = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching trusts: {e}")
        trusts_data = []
    finally:
        cursor.close()
        conn.close()
    return render_template('trust.html', trusts=trusts_data, user=session.get('user'))

if __name__=='__main__':
    app.run(debug=True)
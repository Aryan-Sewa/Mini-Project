from flask import Flask,request,render_template,redirect,flash
from register import Registration
from signin import Signin
from trustregister import TrustRegistration
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'users.json')
json_path1 = os.path.join(base_dir, 'users.json')


print(f"Resolved JSON Path: {json_path}")

app = Flask(__name__)
app.secret_key = 'jojo'

reg = Registration(json_path)
sig = Signin(json_path)
trus = TrustRegistration(json_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/signin', methods=['GET','post'])
def signin():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        
        is_signedin, message = sig.check_signin(user_email, user_password)
        if not is_signedin:
            flash(message)
            return redirect('/register/user')
        else:
            return redirect('/')
        
    return render_template('signin.html')

#for user
@app.route('/register/user', methods=['GET','POST'])
def register():
  
    if request.method == 'POST':
        username = request.form['login-name']
        userphone = request.form['login-phone']
        email = request.form['login-email']
        password = request.form['login-password']

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
    
    return render_template('register.html')

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
    
    return render_template('register.html')


@app.route('/user')
def user():
    return render_template('user.html')

if __name__=='__main__':
    app.run(debug=True)
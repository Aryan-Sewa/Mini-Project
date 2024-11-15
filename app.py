from flask import Flask,request,render_template,jsonify
import json


app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login/user', methods=['GET','POST'])
def user_login():
    islogged = False
    if(not islogged):
        islogged=True
        return render_template('login.html')

    if (islogged):
        username = request.form.get('login-name')
        userphone = request.form.get('login-phone')
        useremail = request.form.get('login-email')
        password = request.form.get('login-password')

        user_data = {
            "user_name": username,
            "phone_no": userphone,
            "email": useremail,
            "pass_word": password
        }

        with open('user_login_data.json', 'w') as json_file:
            json.dump(user_data, json_file, indent=4)
        
        return jsonify({"message": "User login data saved successfully"}), 200

@app.route('/signup/organization', methods=['POST'])
def organization_signup():
    org_name = request.form.get('signup-organization-name')
    org_type = request.form.get('signup-organization-type')
    tax_id = request.form.get('signup-tax-id')
    contact_name = request.form.get('signup-contact-name')
    contact_email = request.form.get('signup-contact-email')
    contact_phone = request.form.get('signup-contact-phone')
    address = request.form.get('signup-address')
    document = request.form.get('signup-document')
    password = request.form.get('signup-password')

    org_data = {
        "organization_name": org_name,
        "organization_type": org_type,
        "tax_id": tax_id,
        "contact_name": contact_name,
        "contact_email": contact_email,
        "contact_phone": contact_phone,
        "address": address,
        "document": document,
        "password": password
    }

    with open('organization_signup_data.json', 'w') as json_file:
        json.dump(org_data, json_file, indent=4)
    
    return jsonify({"message": "Organization sign-up data saved successfully"}), 200


@app.route('/user')
def user():
    return render_template('user.html')

if __name__=='__main__':
    app.run(debug=True)
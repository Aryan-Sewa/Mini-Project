from flask import Flask,request,render_template,redirect,flash
from register import Registration


app = Flask(__name__)
app.secret_key = 'jojo'

reg = Registration('users.json')

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
    return render_template('signin.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['login-name']
        userphone = request.form['login-phone']
        email = request.form['login-email']
        password = request.form['login-password']

        is_valid, message = reg.validate_input(email, password)
        if not is_valid:
            flash(message)
            return redirect('/register')
    
        is_registered, message = reg.register_user(username, email, password, userphone)
        if is_registered:
            flash(message)
            return redirect('/signin')
        else:
            flash(message)
            return redirect('/register')
    
    return render_template('register.html')


@app.route('/user')
def user():
    return render_template('user.html')

if __name__=='__main__':
    app.run(debug=True)
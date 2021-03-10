# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'my precious'


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')
    
# route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') \
                or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('welcome'))
    return render_template('index.html', error=error)

@app.route('/admin',methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        if (request.form['adminUsername'] != 'admin') \
                or request.form['adminPassword'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('adminPage'))
    return render_template('admin.html', error=error)

@app.route('/adminPage')
@login_required
def adminPage():
    return render_template('adminPage.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
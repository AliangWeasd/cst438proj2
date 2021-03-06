
# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
from flask_mysqldb import MySQL
import MySQLdb.cursors

# create the application object
app = Flask(__name__)
app.config['MYSQL_USER'] = 'la8jsp9yrvvjmecw'
app.config['MYSQL_PASSWORD'] = 'dz1gz2pnr8awpoc7'
app.config['MYSQL_DB'] = 'b4rpjxyu117cmkvr'
app.config['MYSQL_HOST'] = 'pwcspfbyl73eccbn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
mysql = MySQL(app)

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

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        user = cursor.fetchone()
        if user:
            error = 'Account already exists'
        elif len(password) <= 6:
            error = 'Password must be greater than 6 characters'
            for x in password:
                if x != '!' or x != '@' or x != '#':
                    error = 'Password must contain "!, @, or #"'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL,% s, % s, % s)', (name, username, password, ))
            mysql.connection.commit()
            error = 'Account created'

    return render_template('signUp.html', error=error)
    
@app.route('/')
def home():
    return render_template('homePage.html')

#route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'] 
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            cursor.execute('SELECT * FROM wishlist WHERE wishlist.userID = % s', (user['userID'],))
            wishlists = cursor.fetchall()
            session['user'] = user
            error = 'Logged in'
            return render_template('wishList.html', error=error, loginUser=user, wishlistTable=wishlists)
        else:
            error = 'Incorrect username/password'
    return render_template('login.html', error=error)

@app.route('/admin',methods=['GET', 'POST'])
def admin():
    error = ''
    if request.method == 'POST':
        if (request.form['adminUsername'] != 'admin') \
                or request.form['adminPassword'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('displayUser'))
    return render_template('admin.html', error=error)

@app.route('/adminPage')
def adminPage():
    return render_template('adminPage.html')

@app.route('/welcome')
def welcome():
    #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #cursor.execute('SELECT * FROM wishlist WHERE wishlist.userID = % s', (session['user']['userID'],))
    #session['wishlists'] = cursor.fetchall()

    return render_template('welcome.html')  # render a template


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out.')
    return redirect(url_for('home'))

@app.route('/displayUsers')
def displayUser():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user')
    data = cursor.fetchall()
    return render_template('displayUsers.html',data=data)

@app.route('/delete/<int:id>')
def delete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM user WHERE userID = % s' % (id))
    mysql.connection.commit()
    return redirect(url_for('displayUser'))

@app.route('/deleteList',methods=['GET','POST'])
def deleteList():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM wishlist WHERE wishlistID = %s' % (request.args.get('wishlistID'),))
    mysql.connection.commit()
    cursor.execute('DELETE FROM WishlistItems WHERE wishlistID = %s' % (request.args.get('wishlistID'),))
    mysql.connection.commit()

    return redirect("/wishList")

@app.route('/addList',methods=['GET', 'POST'])
def addList():
    listName = request.form['name']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO wishlist VALUES (NULL, %s, %s)', (listName,session['user']['userID'], ))
    mysql.connection.commit()

    return redirect('/wishList')
    #return render_template('welcome.html', loginUser=session['user'], wishlistTable=session['wishlists'])

@app.route('/wishList', methods=['GET', 'POST'])
def wishlist():
    if 'user' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM wishlist WHERE wishlist.userID = % s', (session['user']['userID'],))
        session['wishlists'] = cursor.fetchall()

        return render_template('wishList.html',loginUser=session['user'], wishlistTable=session['wishlists'])
    else:
        error = 'Login to view wishlists'
        return render_template('login.html', error=error)
    

@app.route('/viewItems', methods=['GET', 'POST'])
def viewItems():
    error = 'none'
    cursor = mysql.connection.cursor()

    listID = request.args.get('wishlistID')

    if request.method == 'POST':
        listID = request.form['wishlistID']
        name = request.form['listName']
        itemURL = request.form['itemURL']
        imageURL = request.form['imageURL']
        description = request.form['description']
        cursor.execute('INSERT INTO WishlistItems VALUES (NULL, %s, %s, % s, % s, % s)', (listID, name, itemURL, imageURL, description,))
        mysql.connection.commit()
        error = 'Wishlist Item Added'
        #Need an alert if a duplicate was found(try/catch)    
        
    cursor.execute('SELECT * FROM WishlistItems WHERE wishlistID = %s',(listID,))
    data = cursor.fetchall()

    return render_template('viewItems.html', error=error, data=data, wishlistID=listID)

@app.route('/editItem/<int:id>')
def editItem(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM WishlistItems WHERE ID = % s' % (id))
    data = cursor.fetchone()

    return render_template('editItem.html', item=data)

@app.route('/confirmEditItem', methods=['GET','POST'])
def confirmEditItem():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    itemID = request.form['itemID']
    listID = request.form['wishlistID']
    name = request.form['listName']
    itemURL = request.form['itemURL']
    imageURL = request.form['imageURL']
    description = request.form['description']

    cursor.execute('UPDATE WishlistItems SET listName = % s, itemURL = % s, imageURL = % s, description = % s WHERE ID = % s', (name, itemURL, imageURL, description, itemID))
    mysql.connection.commit()

    return redirect(url_for('viewItems', wishlistID=listID))

@app.route('/wishlistDelete/<int:id>/<int:wishID>')
def wishlistDelete(id, wishID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM WishlistItems WHERE ID = % s' % (id))
    mysql.connection.commit()

    return redirect(url_for('viewItems', wishlistID=wishID))

@app.route('/testDisplay', methods=['GET'])
def testDisplay():
    error = 'none'
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM WishlistItems')
    data = cursor.fetchall()
    return render_template('testDisplay.html', error=error, data=data)


@app.route('/editUser', methods=['GET', 'POST'])
def editUser():
    error = ''
    if 'user' in session:
        user = session["user"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user')
        data = cursor.fetchone()
        return render_template('editUser.html',error=error,data=data,user=user)
    else:
        error = 'We said to login in again, you silly-billy!'
        return render_template('login.html', error=error)

@app.route('/updateUsername/<int:id>', methods=['GET', 'POST'])
def updateUsername(id):
    error = ''
    if 'user' in session:
        user = session["user"]
        if request.method == 'POST' and 'newUsername' in request.form:
            newUsername = request.form['newUsername']
            cursor = mysql.connection.cursor()
            sql = 'UPDATE user SET username = % s WHERE userID = % s'
            data = (newUsername,id)
            cursor.execute(sql,data)
            mysql.connection.commit()
            error = 'Account updated, please login again'
            session.pop('logged_in', None)
            session.pop('user', None)
            return render_template('updateUsername.html',user=user,error=error)
        return render_template('updateUsername.html',user=user)
    else:
        error = 'We said to login in again, you silly-billy!'
        return render_template('login.html', error=error)

@app.route('/updatePassword/<int:id>', methods=['GET', 'POST'])
def updatePassword(id):
    error = ''
    if 'user' in session:
        user = session["user"]
        if request.method == 'POST' and 'newPassword' in request.form:
            newPassword = request.form['newPassword']
            cursor = mysql.connection.cursor()
            sql = 'UPDATE user SET password = % s WHERE userID = % s'
            data = (newPassword,id)
            cursor.execute(sql,data)
            mysql.connection.commit()
            error = 'Account updated, please login again'
            session.pop('logged_in', None)
            session.pop('user', None)
            return render_template('updatePassword.html',user=user,error=error)
        return render_template('updatePassword.html',user=user)
    else:
        error = 'We said to login in again, you silly-billy!'
        return render_template('login.html', error=error)

@app.route('/deleteAccount/<int:id>')
def deleteAccount(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM user WHERE userID = % s' % (id))
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/ksEditItem')
def ksEditItem():
    return render_template('ksEditItem.html')

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
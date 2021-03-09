from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'la8jsp9yrvvjmecw'
app.config['MYSQL_PASSWORD'] = 'dz1gz2pnr8awpoc7'
app.config['MYSQL_DB'] = 'b4rpjxyu117cmkvr'
app.config['MYSQL_HOST'] = 'pwcspfbyl73eccbn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
mysql = MySQL(app)

@app.route('/')
def index():
	cursor = mysql.connection.cursor()
	cursor.execute("SELECT * from user")
	data = cursor.fetchone()

	#return render_template("index.html")
	return str(data)

@app.route('/addItem')
def admin():
	return null

if __name__ == '__main__':
	app.run(debug=True)

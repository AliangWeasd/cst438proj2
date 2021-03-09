from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
#Retrieving from Database
app.config['MYSQL_USER'] = 'la8jsp9yrvvjmecw'
app.config['MYSQL_PASSWORD'] = 'dz1gz2pnr8awpoc7'
app.config['MYSQL_DB'] = 'b4rpjxyu117cmkvr'
app.config['MYSQL_HOST'] = 'pwcspfbyl73eccbn.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
mysql = MySQL(app)

#Parse Data, put into List

@app.route("/")
def home():
    test_list = ['Item1','Item2','Item3','Item4']
    return render_template('listing.html', your_list=test_list)



if __name__ == "__main__":
    app.run()
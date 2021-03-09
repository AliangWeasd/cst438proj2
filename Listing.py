from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def home():
    test_list = ['Item1','Item2','Item3','Item4']
    return render_template('your_view.html', your_list=test_list)



if __name__ == "__main__":
    app.run()
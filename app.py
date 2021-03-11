from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def addItem():
    return render_template('test_homepage.html')


if __name__ == '__main__':
    app.run()

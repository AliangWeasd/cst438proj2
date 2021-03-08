from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    test_list = ['Item1','Item2','Item3','Item4']
    return "Hello! this is the main page <h1>Hello<h1>"
#return render_template('your_view.html', your_list=your_list)

#This stuff goes in the react I think?
#{% for your_list_element in your_list %}
#      <p>{{ your_list_element }} </p>
#{% endfor %}



if __name__ == "__main__":
    app.run()
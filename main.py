from flask import *


app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

app.run(debug=True)
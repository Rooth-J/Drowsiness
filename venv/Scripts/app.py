from flask import Flask, render_template
from database import collection

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    data = list(collection.find())
    return render_template("dashboard.html", data=data)

app.run(debug=True)

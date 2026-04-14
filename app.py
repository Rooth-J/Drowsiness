from flask import Flask, render_template
from database import collection

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    data = list(collection.find().sort("timestamp", -1))
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)

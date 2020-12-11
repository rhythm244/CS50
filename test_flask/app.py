from flask import Flask , render_template , redirect, request

app = Flask(__name__)

@app.route("/")
def task():
    return render_template("index.html")

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method = "GET":
    return render_template("add.html")
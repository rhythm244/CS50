from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

db = SQL("sqlite:///money.db")

@app.route("/")
def index():
    rows = db.execute("SELECT * FROM finance")
    return render_template("index.html",rows=rows)

""" INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...); 
"""

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        db.execute("INSERT INTO finance (username, password) VALUES (:username,:password)",username=username,password=password)
    return redirect("/")    

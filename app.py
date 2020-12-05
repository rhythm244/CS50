from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

db = SQL("sqlite:///money.db")

@app.route("/")
def index():
    rows = db.execute("SELECT * FROM money")
    return render_template("index.html",rows=rows)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name")
        password = request.form.get("password")
        db.execute("INSERT ")
    return redirect("/")    

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)
#เพื่อเป็นการ clear แคช ของเบาเซอร์ ซึ่งโดยปกติมันจะ reload ทุกๆ 12 ชั่วโมง แต่ในการฝึกผมจะเซตไว้เป็น 0 เพราะแก้โคตรบ่อย
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#config session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#เป็นการบอกโปรแกรมว่า จะใช้ flask ที่ใส่ในตัวแปรของ add นะ ใช้ feature ว่า route
@app.route("/")
def task():
    #ให้โปรแกรม check ว่าใน ข้อมูลใน session มี key todos อยู่หรือไม่ เพราะข้อมูลใน session DICT class
    if "todos" not in session:
        session["todos"] = []
    #ถ้ามีการเรียก => / ให้รีเทินค่า index.html
    # ค่า todos ตัวแรกคือค่าใน index.html ตัวที่สองคือค่าใน app.py
    return render_template("index.html",todos=session["todos"])

#ถ้ามีการเรียก /add ให้ทำฟังชั่น add โดยสามารถมีการกระทำได้ทั้ง GET และ POST
@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    
    #ถ้าไม่ใช่ GET ให้นำค่าที่ได้จาก Form ของหน้า add ที่ถูก POST เอามาใส่ไว้ในตัวแปร
    #จริงๆ บรรทัดล่างนี้ไม่จำเป็นต้องเป็น elif เป็น else ธรรมดา แล้วไม่ต้องมีเงื่อนไขก็ได้ แต่ใส่ไว้จะได้ไม่งง
    elif request.method == "POST":
        #เอาค่า name ="task"ใน add.html มาใส่ไว้ในตัวแปร todo จากการ POST มาของ add.html
        todo = request.form.get("task")
        #ใส่ค่าที่เจอล่าสุดลงไปในตัวแปรที่สร้างไว้ในชื่อว่า session["todos"]
        session["todos"].append(todo)
        #หลังจากนั้นให้กลับไปหน้าแรก
        return redirect("/")
        
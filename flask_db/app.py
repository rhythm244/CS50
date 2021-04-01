from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)
#เพื่อเป็นการ clear แคช ของเบาเซอร์ ซึ่งโดยปกติมันจะ reload ทุกๆ 12 ชั่วโมง แต่ในการฝึกผมจะเซตไว้เป็น 0 เพราะแก้โคตรบ่อย
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
#config session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#เข้าถึง database lecture.db 
#lecture.db มันต้องอยู่ใน folder ที่ทำการรัน ซึ่งเวลาเซต JSON มันไปอยู่ใน CS50 เลยจำเป็นต้องเอา lucture.db ไว้นอก folder flask_db***
db = SQL("sqlite:///lecture.db")
#เป็นการบอกโปรแกรมว่า จะใช้ flask ที่ใส่ในตัวแปรของ add นะ ใช้ feature ว่า route
@app.route("/")
def index():
    #เอาค่าจาก table registants in file lecture.db
    rows = db.execute("SELECT * FROM registants")
    #ถ้ามีการเรียก => / ให้รีเทินค่า index.html และให้ตัวแปรใน index.html ที่ชื่อว่า rows มีค่าเท่ากับ rows ที่เอาค่ามาจาก lucture.db
    return render_template("index.html",rows=rows)
    
#ถ้ามีการเรียก /register ให้ทำฟังชั่น add โดยสามารถมีการกระทำได้ทั้ง GET และ POST
@app.route("/register", methods=["GET","POST"])
def register():
    #ถ้าค่าที่ได้มาเป็น GET ทำการเปิดหน้า register.html
    if request.method == "GET":
        return render_template("register.html")
 
    #แต่ถ้าเป็น POST ให้.....check ก่อนว่าใส่มาครบหรือไม่
    elif request.method == "POST":
        name = request.form.get("name")
        if not name:
            return render_template("apology.html",message="You must provide a name")

        email = request.form.get("email")
        if not email:
            return render_template("apology.html",message="You must provide a email")
  
        db.execute("INSERT INTO registants (name, email) VALUES (:name, :email)",name=name,email=email)
        return redirect("/")
        

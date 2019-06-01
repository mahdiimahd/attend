from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

template_dir = os.path.abspath('./templates')

app = Flask(__name__, template_folder=template_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://keKKEq2xBU:0GN0wgq40e@remotemysql.com:3306/keKKEq2xBU'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


### Test Users table for checking db connection
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.username

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    className = db.Column(db.String(80), unique=True, nullable=False)
    teacherId = db.Column(db.Integer)
    numStudents = db.Column(db.Integer)

    def __init__(self, className, teacherId, numStudents):
        self.className = className
        self.teacherId = teacherId
        self.numStudents = numStudents

    def __repr__(self):
        return "Class {} {}".format(self.className, self.teacherId)

class SingleClass(db.model):
    id = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(80), unique=True)
    date = db.Column(db.DateTime, default=)
    className = db.Column(db.String(30))

    def __init__(self, studentName, )



class Classrooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroomName = db.Column(db.String(80), unique=True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __init__(self, classroomName, lat, lng):
        self.classroomName = classroomName
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return "{} {},{}".format(self.classroomName, self.lat, self.lng)

#db.create_all()

#classroom = Classrooms('1003 EECS', 42.292756,-83.714665)
#db.session.add(classroom)
#db.session.commit()

print(Classrooms.query.all())
# admin = User('admin', 'admin@example.com')

# db.session.add(admin)

# print(admin)
# db.session.commit() # This is needed to write the changes to database

# print(User.query.all())

# print(User.query.filter_by(username='admin').first())


## TODO - Import coordinates for classrooms
## Create student signup process
# Create API endpoints for 1. creating new class and table 2. student signup 3. Exporting attendance table to csv and emailing it
# Create nice looking form input
# Create database of EECS professors

@app.route("/class", methods=["GET", "POST"])
def add_class():
    if request.method == "POST":
        newClass = Classes('eecs442','1','0')
        db.session.add(newClass)
        print(newClass)
        db.session.commit()
        return render_template('location.html')
    else:
        teacherId = request.args.get("teacherId")
        print("Teacher Id {}".format(teacherId))
        

@app.route("/", methods=["GET", "POST"])
def firstPage():
    return render_template('location.html')

@app.route("/<className>", methods = ["GET","POST"])
def index(className):
    print(className)
    return render_template('location.html')

def testing():
    if request.method == "POST":
        print("post request worked")
    return render_template('location.html')


     






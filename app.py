from flask import Flask, render_template, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


template_dir = os.path.abspath('./templates')
static_dir = os.path.abspath('./templates/assets')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='')

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
    teacherName = db.Column(db.String(80))
    teacherUniqname = db.Column(db.String(80))
    numStudents = db.Column(db.Integer)
    classroomName = db.Column(db.String(80))

    def __init__(self, className, teacherName, teacherUniqname, classroomName):
        self.className = className.replace(" ","").lower()
        self.classroomName = classroomName
        self.teacherName = teacherName
        self.teacherUniqname = teacherUniqname
        self.numStudents = 0


    def __repr__(self):
        return "Class {} taught by {} of {}".format(self.className, self.teacherName, self.teacherUniqname)

class Singleclass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(80)) 
    date = db.Column(db.DateTime, default=datetime.now())
    className = db.Column(db.String(30))
    uniqname = db.Column(db.String(80))


    def __init__(self, studentName, className, uniqname):
        self.studentName = studentName
        self.className = className
        self.uniqname = uniqname
        self.date = datetime.now()

    
    def __repr__(self):
        return "{} with uniqnam {} in {} on {}".format(self.studentName, self.uniqname, self.className, self.date)



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

db.create_all()

#classroom = Classrooms('1003 EECS', 42.292756,-83.714665)
#db.session.add(classroom)
#db.session.commit()

#print(Classrooms.query.all())
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

@app.route("/addClass", methods=["POST"])
def addClass():
    if request.method == 'POST':
        newClass = Classes(request.form["className"], request.form["teacherName"], request.form["teacherUniqname"], request.form["classroomName"])
        db.session.add(newClass)
        db.session.commit()
        print(newClass)
        return jsonify(
            message="New class created",
            url="https://www.attendapp.me/" + newClass.className
        )


@app.route("/getClasses/<teacherUniqname>", methods=["GET","POST"])
def getClasses(teacherUniqname):
    if request.method == 'GET':
        class_list = Classes.query.filter_by(teacherUniqname=teacherUniqname).distinct().all()
        class_list_response = [str(c.className) for c in class_list]
        print(class_list_response)
        return jsonify(
            classes=class_list_response
        )

@app.route("/getClasses", methods=["GET","POST"])
def getAllClasses():
    if request.method == 'GET':
        class_list = Classes.query.all()
        class_list_response = [str(c.className) for c in class_list]
        print(class_list_response)
        return jsonify(
            classes=class_list_response
        )



@app.route("/c/<className>", methods = ["GET","POST"])
def index(className):
    if request.method == 'POST':
        print("post request received")
        # print(request.data.keys())
        print(datetime.now())
        entry = Singleclass(request.form['studentName'], className, request.form['uniqname'])
        print(entry)
        db.session.add(entry)
        db.session.commit()
        return "{ 'Status' : 'OK'}"
    else:
        print("Get request received")
        return render_template('location.html', value=className, )

@app.route("/attendance/<classname>", methods = ["GET"])
def getAttendance(classname):
    if request.method == 'GET':
        list_students = Singleclass.query.filter_by(className=classname).all()
        num_students = Singleclass.query.with_entities(Singleclass.uniqname).distinct().all()
        print(num_students)
        return jsonify(
            count=len(num_students),
        )

# def testing():
#     if request.method == "POST":
#         print("post request worked")
#     return render_template('location.html')

if __name__ == '__main__':
    app.run(debug=True)



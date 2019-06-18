from flask import Flask, render_template, request, jsonify, send_file
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone
import csv


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
    mondayClass = db.Column(db.String(80))
    tuesdayClass = db.Column(db.String(80))
    wednesdayClass = db.Column(db.String(80))
    thursdayClass = db.Column(db.String(80))
    fridayClass = db.Column(db.String(80))
    mondayTime = db.Column(db.Integer)
    tuesdayTime = db.Column(db.Integer)
    wednesdayTime = db.Column(db.Integer)
    thursdayTime = db.Column(db.Integer)
    fridayTime = db.Column(db.Integer)

    def __init__(self, className, teacherName, teacherUniqname, classroomName, mondayClass, mondayTime, tuesdayClass, tuesdayTime, wednesdayClass, wednesdayTime, thursdayClass, thursdayTime, fridayClass, fridayTime):
        self.className = className.replace(" ","").lower()
        self.classroomName = classroomName
        self.teacherName = teacherName
        self.teacherUniqname = teacherUniqname
        self.numStudents = 0
        self.mondayClass = mondayClass
        self.mondayTime = mondayTime
        self.tuesdayClass = tuesdayClass
        self.tuesdayTime = tuesdayTime
        self.wednesdayClass = wednesdayClass
        self.wednesdayTime = wednesdayTime
        self.thursdayClass = thursdayClass
        self.thursdayTime = thursdayTime
        self.fridayClass = fridayClass
        self.fridayTime = fridayTime


    def __repr__(self):
        return "Class {} taught by {} of {}".format(self.className, self.teacherName, self.teacherUniqname)

class Singleclass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(80)) 
    date = db.Column(db.Date)
    className = db.Column(db.String(30))
    uniqname = db.Column(db.String(80))


    def __init__(self, studentName, className, uniqname):
        self.studentName = studentName
        self.className = className
        self.uniqname = uniqname
        self.date = datetime.now(timezone('US/Eastern')).date()

    
    def __repr__(self):
        return "{} with uniqnam {} in {} on {}".format(self.studentName, self.uniqname, self.className, self.date)



class Classrooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroomName = db.Column(db.String(80), unique=True)
    lat = db.Column(db.Numeric(2,7))
    lng = db.Column(db.Numeric(2,7))

    def __init__(self, classroomName, lat, lng):
        self.classroomName = classroomName
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return "{} {},{}".format(self.classroomName, self.lat, self.lng)

db.create_all()
db.session.commit()
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
        newClass = Classes(
            className=request.form["className"],
            teacherName=request.form["teacherName"],
            teacherUniqname=request.form["teacherUniqname"],
            classroomName=request.form["classroomName"],
            mondayClass=request.form["mondayClass"],
            mondayTime=request.form["mondayTime"],
            tuesdayClass=request.form["tuesdayClass"],
            tuesdayTime=request.form["tuesdayTime"],
            wednesdayClass=request.form["wednesdayClass"],
            wednesdayTime=request.form["wednesdayTime"],
            thursdayClass=request.form["thursdayClass"],
            thursdayTime=request.form["thursdayTime"],
            fridayClass=request.form["fridayClass"],
            fridayTime=request.form["fridayTime"])
        db.session.add(newClass)
        db.session.commit()
        print(newClass)
        return jsonify(
            message="New class created",
            url="https://www.attendapp.me/c/" + newClass.className
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

@app.route("/getClass/<className>", methods=["GET"])
def getClassInfo(className):
    if request.method == 'GET':
        class_info = Classes.query.filter_by(className=className).first()
        classroom_info = Classrooms.query.filter_by(classroomName=class_info.classroomName).first()

        return jsonify(
            teacherName=class_info.teacherName,
            roomInfo=classroom_info.classroomName,
            lat=classroom_info.lat,
            lng=classroom_info.lng,
        )


@app.route("/c/<className>", methods = ["GET","POST"])
def index(className):
    if request.method == 'POST':
        print("post request received")
        # print(request.data.keys())

        classInfo = Classes.query.filter_by(className=className).first()
        print(classInfo)
        date = datetime.now(timezone('US/Eastern'))
        day = date.weekday()
        is_day_valid = ""
        is_time_valid = ""
        if day == 0:
            is_day_valid = classInfo.mondayClass
            is_time_valid = classInfo.mondayTime
        elif day == 1:
            is_day_valid  = classInfo.tuesdayClass
            is_time_valid = classInfo.tuesdayTime
        elif day == 2:
            is_day_valid = classInfo.wednesdayClass
            is_time_valid = classInfo.wednesdayTime
        elif day == 3:
            is_day_valid = classInfo.thursdayClass
            is_time_valid = classInfo.thursdayTime
        elif day == 4:
            is_day_valid = classInfo.fridayClass
            is_time_valid = classInfo.fridayTime
        else:
            is_day_valid = "False"
            is_time_valid = -1
        print(day, is_day_valid, is_time_valid, date.hour)
        if is_day_valid == "False":
            return jsonify(
                message="Class is not happening today"
            )
        if is_time_valid != date.hour:
            return jsonify(
                message="Class is not in session right now"
            )

        last_record = Singleclass.query.filter_by(className=className).filter_by(uniqname=request.form['uniqname']).order_by(Singleclass.date.asc()).all()
        if len(last_record) > 0:
            last_record = last_record[-1]
            if last_record.date.date() == date.date():
                return jsonify(
                    message="You have already checked in today."
                )
        entry = Singleclass(request.form['studentName'], className, request.form['uniqname'])
        print(entry)
        db.session.add(entry)
        db.session.commit()
        return jsonify(
            message="You are now checked in!"
        )
    else:
        print("Get request received")
        return render_template('signin.html', value=className )

@app.route("/attendance/<classname>", methods = ["GET"])
def getAttendance(classname):
    if request.method == 'GET':
        print()
        list_students = Singleclass.query.filter_by(className=classname).with_entities(Singleclass.uniqname).distinct().all()
        #num_students = Singleclass.query.with_entities(Singleclass.uniqname).distinct().all()
        classroom_name = Classes.query.filter_by(className=classname).first()
        professorName = classroom_name.teacherName
        classroomName = classroom_name.classroomName
        print(list_students,classroomName)
        return jsonify(
            count=len(list_students),
            classroom=classroomName,
            teacherName=professorName
        )

@app.route("/classroom", methods=["GET","POST"])
def addClassroom():
    if request.method == 'POST':
        classroom = Classrooms(request.form["roomNumber"] + " " + request.form["buildingName"], request.form["lat"] , request.form["lng"])
        db.session.add(classroom)
        db.session.commit()
        return jsonify(
            message="Building added"
        )
    else:
        list_classrooms = Classrooms.query.all()
        classrooms = {}
        for c in list_classrooms:
            classrooms[str(c.classroomName)] = str(c.lat) + "," + str(c.lng)
        print (classrooms)
        return jsonify(
            classrooms
        )

@app.route("/toCSV/<className>", methods=["GET"])
def toCSV(className):
    if request.method == 'GET':
        dates = Singleclass.query.filter_by(className=className).with_entities(Singleclass.date).order_by(Singleclass.date.asc()).distinct().all()
        students = Singleclass.query.filter_by(className=className).all()
        # print(dates[0].strftime("%m/%d/%Y, %H:%M:%S"))
        # dateObjects = [str(d) for d in dates]
        print(students)

        
        # students = Singleclass.query.filter_by(date=dates[0]).all()
        #csvData = [['Person', 'Age'], ['Peter', '22'], ['Jasmine', '21'], ['Sam', '24']]
        csvData = [ [student.uniqname,'1'] for student in students]
        with open('person.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Name','06/12/2019'])
            writer.writerows(csvData)
        return send_file('person.csv', attachment_filename='person.csv')

        # return jsonify(
        #     message="File sent"
        # )
# def testing():
#     if request.method == "POST":
#         print("post request worked")
#     return render_template('location.html')

if __name__ == '__main__':
    app.run(debug=True)



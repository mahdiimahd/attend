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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
    def __repr__(self):
        return '<User %r>' % self.username

admin = User('admin', 'admin@example.com')

db.session.add(admin)

print(admin)
db.session.commit() # This is needed to write the changes to database

print(User.query.all())

print(User.query.filter_by(username='admin').first())

@app.route("/")
def hello():
    return render_template('location.html')



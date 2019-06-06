from flask import Flask, render_template
import os

template_dir = os.path.abspath('./templates')

app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def hello():
    return render_template('location.html')

@app.route("/teacher")
def overview():
    return render_template('teacher.html')


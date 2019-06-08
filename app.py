from flask import Flask, render_template
import os

template_dir = os.path.abspath('./templates')
static_dir = os.path.abspath('./templates/assets')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='')

@app.route("/")
def hello():
    return render_template('location.html')



if __name__ == '__main__':
    app.run(debug=True)



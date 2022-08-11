from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    latest = 'latest.jpg'
    return render_template('index.html', latest=latest)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
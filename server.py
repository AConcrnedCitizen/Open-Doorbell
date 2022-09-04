from crypt import methods
from urllib import request
from flask import Flask, render_template, url_for, request
import takephoto as photo
import time
import tts
from pydub import AudioSegment
from pydub.playback import play

app = Flask(__name__)

shuttersound = AudioSegment.from_file("shutter.mp3", format="mp3")


@app.route('/')
def page():
    return render_template('index.html')


@app.route('/take_photo')
def takephoto():
    photo.takephoto()
    play(shuttersound)
    time.sleep(5)
    return("nothing")


@app.route('/', methods=['POST'])
def speak():
    text = request.form['text']
    tts.speak(text)
    print("text")
    p_text = text.upper()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

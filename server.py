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

@app.route('/', methods=["GET", "POST"])
def page():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        if request.form.get('action1') == "Take Photo":
            photo.takephoto()
            play(shuttersound)

        elif request.form.get('action2') == "Speak":
            text = request.form['text']
            if text != "":
                tts.speak(str(text).upper())
                print("Speaking")
            else:
                pass
    else:
        return render_template('index.html')
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

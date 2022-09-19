from flask import Flask, render_template, Response, request,redirect,url_for,send_from_directory
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread 
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import binascii


global capture,rec_frame, grey, switch, neg, face, rec, out 
rec_frame = None
capture=0
switch=1
rec=0

#shuttersound = AudioSegment.from_file("shutter.mp3", format="mp3")

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')
camera = cv2.VideoCapture(0)

def encode(x):
    return binascii.hexlify(x.encode('utf-8')).decode()

def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 125)
    engine.say(str(text))
    engine.runAndWait()

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read()
        if success:   
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
            
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if request.form.get('action1') == "Take Photo":
            global capture
            capture=1
            print("Photo Taken")
            #play(shuttersound)
        elif request.form.get('action2') == 'Speak':
            text = request.form['text']
            if text != "":
                speak(str(text).upper())
                print("Speaking")
            else:
                pass
        return redirect(url_for('index'))
    elif request.method=='GET':
        return render_template('index.html')

@app.route('/gallery')
def gallery():
    root_dir = "./shots"
    type = ""
    image_paths = []
    for root,dirs,files in os.walk(root_dir):
        for file in files:
            if file.endswith(".png"):
                type = "img"
            elif file.endswith(".mp4"):
                type = "vid"
            image_paths.append([encode(os.path.join(root,file)), type])
    return render_template('gallery.html', paths=image_paths)

@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir,filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1

        elif  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(0)
                switch=1
        elif  request.form.get('rec') == 'Start/Stop Recording':
            global rec, out
            rec= not rec
            if(rec):
                now=datetime.datetime.now() 
                fourcc = cv2.VideoWriter_fourcc(*'x264')
                out = cv2.VideoWriter('./shots/vid_{}.mp4'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
                #Start new thread for recording the video
                thread = Thread(target = record, args=[out,])
                thread.start()
            elif(rec==False):
                out.release()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()     
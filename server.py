from flask import Flask, render_template, url_for
#import takephoto
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def page(): 
    return render_template('index.html')


@app.route('/background_process_test')
def background_process_test():
    #print ("SCREAM")
    return ("nothing")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
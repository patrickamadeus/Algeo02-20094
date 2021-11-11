from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image
import base64
import io
from compress.compress import *


app = Flask(__name__)
UPLOAD_FOLDER = 'static/assets/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url) 
    file = request.files['file']
    rate = request.form['rate']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        basename = filename + "-ori"
        text = "Compression process for " + filename + " finished"

        #save image original
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], basename))
        #main process on compressing image
        img_str, secs = main(file, int(rate))

        #decode base64 jadi image lagi
        image = base64.b64decode(img_str)       
        img = Image.open(io.BytesIO(image))

        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(rate + ' % compressed in '+str(round(secs,3))+' s')
        return render_template('index.html', filename=filename, basename = basename, text=text)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='assets/' + filename), code=301)
# @app.route('/')
# def index():
#     return render_template("index.html")

# @app.route('/result', methods= ['POST','GET'])
# def result():
#     rate = request.form.to_dict()
#     print(post)
#     new = rate['post']
#     return render_template('index.html',rate = new)

# @app.route('/getresult', methods= ['POST','GET'])
# def resulttest():
#     data = request.form.to_dict()
#     print(data)
#     new = data['rate']
#     return render_template('index.html',post = new)

if __name__ == '__main__':
    app.run(debug = True)
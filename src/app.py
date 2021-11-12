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
        ori_image = Image.open(file)
        data = io.BytesIO()
        ori_image.save(data,"PNG")
        encoded_ori_image = base64.b64encode(data.getvalue())

        #save compressed image via main function from compress.py
        encoded_image, secs = main(file, int(rate))

        flash(rate + ' % compressed in '+str(round(secs,3))+' s')
        return render_template('index.html', filename=encoded_image.decode('utf-8'), basename = encoded_ori_image.decode('utf-8'), text=text)


if __name__ == '__main__':
    app.run(debug = True)
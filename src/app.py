from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image
import base64
import io
from compress.compress import *

app = Flask(__name__)
app.secret_key = "secret key"
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    #get File dan Rate dari form submission
    file = request.files['file']
    rate = request.form['rate']

    #penamaan file
    filename = secure_filename(file.filename)
    basename = filename + "-ori"

    #save image original
    ori_image = Image.open(file)
    img_format = ori_image.format
    data = io.BytesIO()
    ori_image.save(data,img_format)
    encoded_ori_image = base64.b64encode(data.getvalue())

    #save compressed image via main function from compress.py
    encoded_image, secs, percent = main(file, int(rate))

    #String yang akan di-render ke HTML page
    text = "Compression process for " + filename + " finished in " + str(round(secs,3)) + " s"
    flash(rate + ' % compressed')
    return render_template('index.html', filename=encoded_image.decode('utf-8'), basename = encoded_ori_image.decode('utf-8'),percent = percent, text=text, img_format= img_format)


if __name__ == '__main__':
    app.run(debug = True)
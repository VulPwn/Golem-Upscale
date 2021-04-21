import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from pathlib import Path
import time

secret_key = os.urandom(12)

UPLOAD_FOLDER = Path(__file__).parent.parent.absolute() / "data/"
DOWNLOAD_FOLDER = Path(__file__).parent.parent.absolute() / "result"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['SECRET_KEY'] = secret_key
bootstrap = Bootstrap(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file found')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template("file_upload.html")

@app.route('/<filename>')
def uploaded_file(filename):
    if app.config['DOWNLOAD_FOLDER'] / filename:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        flash('Upscaling needs a little more time...')

@app.route('/run_requestor')
def requestor():
    time.sleep(10)
    os.system('python requestor.py')
    flash('requestor running now...')
    return

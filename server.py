#!/usr/bin/env python3

from backend.api import API
import os
from flask import Flask, render_template, request
import config
from werkzeug.utils import secure_filename

app = Flask(
    config.APP_NAME,
    template_folder='./frontend',
    static_folder='./frontend/static',
)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
API.setRootPath(app.root_path)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route("/")
def root():
    return render_template('index.html')


@app.route("/api/upload")
def api_upload():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return API.upload(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "Error"


@app.route("/api/image_list")
def api_image_list():
    return "Image List"


@app.route("/api/test")
def test():
    return API.test()


if __name__ == "__main__":
    # run debug server
    app.run(host='127.0.0.1', port=5050, debug=True)

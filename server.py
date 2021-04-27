#!/usr/bin/env python3

from flask import (
    Flask, 
    render_template, 
    request, 
    abort, 
    jsonify,
    send_from_directory,
)
from flask_sqlalchemy import SQLAlchemy

import os.path 
import uuid
import time
from datetime import datetime 
import config


### FLASK INITIALIZATION

app = Flask(
    config.APP_NAME, 
    template_folder=config.TEMPLATE_PATH,
    static_folder=config.STATIC_PATH,
)

app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
db = SQLAlchemy(app)


### MODELS

class ImageItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


### HELPER FUNCTIONS

def map_image_item(item):
    return {
        'id': item.id,
        'username': item.username,
        'image_url': item.image_path,
        'timestamp': str(item.timestamp),
    }

def success_resp(data):
    return jsonify({
        'status': 'success',
        **data,
    })

def error_resp(msg):
    return jsonify({
        'status': 'error', 
        'message': msg,
    })


### ROUTES

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/api/upload", methods=['POST'])
def api_upload():
    print(request.files)
    if 'image' not in request.files:
        return error_resp('Input image not present')

    username = request.form.get('username', None)
    filter = request.form.get('filter', None)

    if username is None or filter is None:
        return error_resp('Please fill all the required fields')

    input_image = request.files['image']
    print(input_image.filename)

    if not '.' in input_image.filename:
        return error_resp('Invalid filename')

    extension = input_image.filename.split('.')[-1]
    filename = '{}.{}.{}'.format(
        str(uuid.uuid4()),
        int(time.time()),
        extension,
    )
    
    input_image.save(os.path.join(config.MEDIA_PATH, filename))
    success = True # process(input_image.stream, filename)

    if success:
        return success_resp({
            'image_url': '/{}/{}'.format(
                config.MEDIA_PATH,
                filename,
            ),
        })

    return error_resp('Image processing failed, please try again later')

@app.route("/api/list_images")
def api_list_images():
    items = ImageItem.query.order_by(ImageItem.timestamp.desc()).limit(20).all()
    return success_resp({
        'data': list(map(map_image_item, items)),
    })

@app.route("/media/<path:path>")
def serve_media(path):
    return send_from_directory(config.MEDIA_PATH, path)

if __name__ == "__main__":
    # run debug server
    app.run(host='127.0.0.1', port=5050, debug=True)

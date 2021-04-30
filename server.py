#!/usr/bin/env python3

from flask import (
    Flask, 
    render_template, 
    request, 
    jsonify,
    send_from_directory,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc

import os
import uuid
import time
from datetime import datetime 

import config
from backend.api import API


### FLASK INITIALIZATION

app = Flask(
    config.APP_NAME, 
    template_folder=config.TEMPLATE_PATH,
    static_folder=config.STATIC_PATH,
)

app.config['MAX_CONTENT_LENGTH'] = config.MAX_UPLOAD_SIZE
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
db = SQLAlchemy(app)


### MODELS

class ImageItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    filter_used = db.Column(db.String(255), nullable=False)
    face_count = db.Column(db.Integer, nullable=False)
    visible = db.Column(db.Boolean, nullable=False, default=True)


### HELPER FUNCTIONS

def map_image_item(item):
    return {
        'id': item.id,
        'username': item.username,
        'image_url': url_for('serve_processed_media', path=item.image_filename),
        'filter_used': item.filter_used,
        'face_count': item.face_count,
        'timestamp': int(item.timestamp.timestamp()), # in UTC timezone
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
    return render_template('index.html', 
        app_name = config.APP_NAME,
    )

@app.route("/api/upload", methods=['POST'])
def api_upload():
    if 'image' not in request.files:
        return error_resp('Input image not present')

    username = request.form.get('username', None)
    filter_name = request.form.get('filter', None)
    visible = not (request.form.get('private', None) == 'on')

    if username is None or filter_name is None:
        return error_resp('Please fill all the required fields')

    if len(username) < 3 or len(username) > 255:
        return error_resp('Name must be between 3 and 255 characters')

    if filter_name not in config.ALLOWED_FILTER_NAMES:
        return error_resp('Invalid filter')

    input_image = request.files['image']
    if '.' not in input_image.filename:
        return error_resp('Invalid filename')

    extension = input_image.filename.rsplit('.', 1)[1].lower()
    if extension not in config.ALLOWED_EXTENSIONS:
        return error_resp('Extension not allowed, only "{}" are allowed'.format(
            ', '.join(config.ALLOWED_EXTENSIONS)
        ))

    filename = '{}.{}.{}'.format(
        str(uuid.uuid4()),
        hex(int(time.time() * 1000) ^ 0x69deadbeef)[2:],
        extension,
    )
    
    original_path = os.path.join(config.ORIGINAL_MEDIA_PATH, filename)
    input_image.save(original_path)
   
    success = False
    faces_detected = 0

    try:
        # TODO: return number of faces detected and accept filter name
        # (success, faces_detected) = API.process(filename, filter_name)
        success = API.process(filename, filter_name)
        faces_detected = 1 # Remove when API is implemented
    except Exception:
        pass

    if success and faces_detected > 0:
        try:
            image_item = ImageItem(
                username = username,
                image_filename = filename,
                filter_used = filter_name,
                face_count = faces_detected,
                visible = visible,
            )

            db.session.add(image_item)
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError:
            return error_resp('Database error, please try again later')

        return success_resp({
            'image_url': url_for('serve_processed_media', path=filename),
        })
      
    # Delete original image and return error message
    os.remove(original_path)

    if not success:
        return error_resp('Image processing failed, please try again later')

    # Face count is 0
    return error_resp('Unable to detect faces in supplied image')

@app.route("/api/list_images")
def api_list_images():
    try:
        items = ImageItem.query\
                    .filter_by(visible=True)\
                    .order_by(ImageItem.timestamp.desc())\
                    .limit(20)\
                    .all()

    except sqlalchemy.exc.SQLAlchemyError:
        return error_resp('Database error, please try again later')

    return success_resp({
        'count': len(items),
        'data': list(map(map_image_item, items)),
    })

@app.route("/media/proc/<path:path>")
def serve_processed_media(path):
    return send_from_directory(config.PROCESSED_MEDIA_PATH, path)

@app.route("/media/orig/<path:path>")
def serve_original_media(path):
    return send_from_directory(config.ORIGINAL_MEDIA_PATH, path)


### DEBUG SERVER ENTRYPOINT

@app.route("/api/test")
def test():
    return API.test()

if __name__ == "__main__":
    # run debug server
    app.run(host='127.0.0.1', port=5050, debug=True)

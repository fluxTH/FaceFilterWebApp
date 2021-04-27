import os
import face_recognition
from PIL import Image, ImageDraw
import config


class API:

    ROOT_PATH = ""
    FILTER_PATH = ""

    @staticmethod
    def setRootPath(rootPath):
        API.ROOT_PATH = rootPath
        API.FILTER_PATH = os.path.join(API.ROOT_PATH, config.FILTER_FOLDER)

    @staticmethod
    def upload(filepath):
        image = face_recognition.load_image_file(filepath)
        face_location_list = face_recognition.face_locations(image)
        face_landmarks_list = face_recognition.face_landmarks(image)
        return "Uploaded"

    @staticmethod
    def test():
        return str(os.listdir(API.FILTER_PATH))

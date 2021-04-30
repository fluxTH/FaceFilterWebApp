import os
import face_recognition
from PIL import Image, ImageDraw
import config
import random


class API:

    @staticmethod
    def process(filename):
        filter_image_list = os.listdir(config.FILTER_PATH)
        random_filter_image = filter_image_list[random.randint(
            0, len(filter_image_list) - 1)]

        image = face_recognition.load_image_file(
            os.path.join(config.ORIGINAL_MEDIA_PATH, filename))
        face_location_list = face_recognition.face_locations(image)
        face_landmarks_list = face_recognition.face_landmarks(image)
        filter_image = Image.open(os.path.join(
            config.FILTER_PATH, random_filter_image)).convert("RGBA")
        filter_part = random_filter_image.split("_")[0]
        process_image = Image.fromarray(image)

        for face_location in face_location_list:
            # top right bottom left
            d = ImageDraw.Draw(process_image, "RGB")
            d.rectangle((face_location[3], face_location[0],
                         face_location[1], face_location[2]), outline=(0, 0, 0))
            width = face_location[1] - face_location[3]
            height = face_location[2] - face_location[0]
            print(face_location)

            if filter_part == "hat":
                ratio = width / filter_image.size[0] * 1.4
                filter_image = filter_image.resize(((int)(filter_image.size[0] * ratio), (int)(filter_image.size[1] * ratio)))
                filter_pos = (face_location[3] -(int)((filter_image.size[0] - width) / 2),face_location[0] - filter_image.size[1])
                print(filter_pos)
                process_image.paste(filter_image, filter_pos,mask=filter_image.split()[3])
            
            elif filter_part == "float":
                ratio = width / filter_image.size[0] * 3.0
                filter_image = filter_image.resize(((int)(filter_image.size[0] * ratio), (int)(filter_image.size[1] * ratio)))
                filter_pos = (face_location[3] -(int)((filter_image.size[0] - width) / 2),face_location[0] - filter_image.size[1])
                print(filter_pos)
                process_image.paste(filter_image, filter_pos,mask=filter_image.split()[3])

        for face_landmarks in face_landmarks_list:
            if filter_part == "glass":
                ratio = width / filter_image.size[0] * 1.0
                left_eye = face_landmarks['left_eye']
                print(left_eye)
                filter_image = filter_image.resize(((int)(filter_image.size[0] * ratio), (int)(filter_image.size[1] * ratio)))
                filter_pos = ((int)(left_eye[0][0] - filter_image.size[1]/2),(int)(left_eye[0][1] - filter_image.size[1]/2))

                print(filter_pos)
                process_image.paste(filter_image, filter_pos,
                                    mask=filter_image.split()[3])
            
            

        process_image.save(os.path.join(config.PROCESSED_MEDIA_PATH, filename))
        return True

    @staticmethod
    def test():
        return str()

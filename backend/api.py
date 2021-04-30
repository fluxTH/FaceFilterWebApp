import os
import face_recognition
from PIL import Image, ImageDraw
import config
import random


class API:

    @staticmethod
    def getFilterTupleList():
        return [(e, e[e.find('_')+1:e.rfind('.')]) for e in API.getFilterList()]

    @staticmethod
    def getFilterList():
        return os.listdir(config.FILTER_PATH)

    @staticmethod
    def process(filename, filter_name):
        filter_image_list = API.getFilterList()

        if (filter_name not in filter_image_list):
            filter_name = filter_image_list[random.randint(
                0, len(filter_image_list) - 1)]
            filter_part = filter_name.split("_")[0]
        else:
            filter_part = filter_name.split("_")[0]

        try:
            image = face_recognition.load_image_file(
                os.path.join(config.ORIGINAL_MEDIA_PATH, filename))
            face_location_list = face_recognition.face_locations(image)
            face_landmarks_list = face_recognition.face_landmarks(image)
            filter_image = Image.open(os.path.join(
                config.FILTER_PATH, filter_name)).convert("RGBA")
            process_image = Image.fromarray(image)

            for face_location in face_location_list:

                # draw rectangle around face
                # top right bottom left
                d = ImageDraw.Draw(process_image, "RGB")
                d.rectangle((face_location[3], face_location[0],
                             face_location[1], face_location[2]), outline=(0, 0, 0))
                width = face_location[1] - face_location[3]
                height = face_location[2] - face_location[0]

                if filter_part == "hat":
                    ratio = width / filter_image.size[0] * 1.4
                    filter_image = filter_image.resize(
                        ((int)(filter_image.size[0] * ratio), (int)(filter_image.size[1] * ratio)))
                    filter_pos = (face_location[3] - (int)(
                        (filter_image.size[0] - width) / 2), face_location[0] - filter_image.size[1])
                    process_image.paste(filter_image, filter_pos,
                                        mask=filter_image.split()[3])

                elif filter_part == "float":
                    ratio = width / filter_image.size[0] * 3.0
                    filter_image = filter_image.resize(
                        ((int)(filter_image.size[0] * ratio), (int)(filter_image.size[1] * ratio)))
                    filter_pos = (face_location[3] - (int)(
                        (filter_image.size[0] - width) / 2), face_location[0] - filter_image.size[1])
                    print(filter_pos)
                    process_image.paste(filter_image, filter_pos,
                                        mask=filter_image.split()[3])

            for face_landmarks in face_landmarks_list:
                if filter_part == "glass":
                    ratio = width / filter_image.size[0] * 1.0
                    left_eye = face_landmarks['left_eye']
                    print(left_eye)
                    filter_image = filter_image.resize(
                        ((int)(filter_image.size[0] * ratio), (int)(filter_image.size[1] * ratio)))
                    filter_pos = ((int)(left_eye[0][0] - filter_image.size[1]/2),
                                  (int)(left_eye[0][1] - filter_image.size[1]/2))

                    print(filter_pos)
                    process_image.paste(filter_image, filter_pos,
                                        mask=filter_image.split()[3])
                elif filter_part == "nose":
                    ratio = width / filter_image.size[0] * 1.2
                    nose_tip = face_landmarks['nose_tip']
                    print(nose_tip)
                    filter_image = filter_image.resize(
                        ((int)(filter_image.size[0] * ratio), (int)(filter_image.size[1] * ratio)))
                    filter_pos = ((int)(nose_tip[0][0] - 1.15*filter_image.size[1]),
                                  (int)(nose_tip[0][1] - filter_image.size[1]/2))

                    print(filter_pos)
                    process_image.paste(filter_image, filter_pos,
                                        mask=filter_image.split()[3])
                elif filter_part == "chin":
                    ratio = width/filter_image.size[0] * 1
                    chin = face_landmarks['chin']
                    # d.polygon(chin, outline=(0, 0, 0))
                    filter_image = filter_image.resize(
                        ((int)(filter_image.size[0] * ratio), (int)(filter_image.size[1] * ratio)))

                    d.polygon(chin, outline=(0, 0, 0))
                    filter_pos = ((int)((sum([e[0] for e in chin]) / len(chin)) - (filter_image.size[0] / 2)),
                                  (int)((sum([e[1] for e in chin]) / len(chin)) - (filter_image.size[1] / 4)))
                    process_image.paste(
                        filter_image, filter_pos, mask=filter_image.split()[3])
                print(face_landmarks)

            process_image.save(os.path.join(
                config.PROCESSED_MEDIA_PATH, filename))
            return (True, len(face_location_list))
        except:
            return (False, 0)

    @staticmethod
    def test():
        return "Test"

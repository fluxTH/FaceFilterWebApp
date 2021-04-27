import face_recognition
from PIL import Image, ImageDraw


def process(image, filter_image, position):
    image = face_recognition.load_image_file(image)
    face_location_list = face_recognition.face_locations(image)
    face_landmarks_list = face_recognition.face_landmarks(image)
    filter_image = Image.open(filter_image).convert("RGBA")

    process_image = Image.fromarray(image)
    #for face_landmarks in face_landmarks_list:
        #print(face_landmarks.keys())
    #dict_keys(['chin', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 'nose_tip', 'left_eye', 'right_eye', 'top_lip', 'bottom_lip'])
    
    for face_location in face_location_list:
        # top right bottom left
        d = ImageDraw.Draw(process_image, "RGB")
        d.rectangle(face_location, outline=(0, 0, 0))
        width = face_location[1] - face_location[3]
        height = face_location[2] - face_location[0]
        print(face_location)

        if position == "head":
            ratio = width / filter_image.size[0] * 1.4
            filter_image = filter_image.resize(
                ((int)(filter_image.size[0] * ratio), (int)(filter_image.size[1] * ratio)))
            filter_pos = (face_location[3] -(int)((filter_image.size[0] - width) / 2),face_location[0] - filter_image.size[0])
            print(filter_pos)
            process_image.paste(filter_image, filter_pos,mask=filter_image.split()[3])

        elif position == "eyes":
            ratio = width / filter_image.size[0] * 1.0
            left_eye = face_landmarks['left_eye']
            right_eye = face_landmarks['right_eye']
            print(left_eye)
            filter_image = filter_image.resize(
                ((int)(filter_image.size[0] * ratio), (int)(filter_image.size[1] * ratio)))
            
            filter_pos = ((int)(left_eye[0][0] - filter_image.size[1]/2) ,(int)(left_eye[0][1] - filter_image.size[1]/2))
            print(filter_pos)
            process_image.paste(filter_image, filter_pos,mask=filter_image.split()[3])
    
    return process_image


#process("backend/demo_image.png", "backend/demo_filter.png", None).show()

process("backend/demo_image_6.jpg", "backend/demo_filter.png", "head").show()
process("backend/demo_image_4.jpg", "backend/cook-hat.png", "head").show()

#process("backend/demo_image.png","backend/sunglasses.png","eyes").show()
#process("backend/demo_image_2.jpg","backend/sunglasses.png","eyes").show()
#process("backend/demo_image_2.jpg","backend/thug-life-sunglasses.png","eyes").show()

#process("backend/demo_image_3.jpg","backend/sunglasses.png","eyes").show()

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import keyboard
import os
import pandas as pd

train_data_path = os.path.join('artifacts', "attendance.csv")
os.makedirs(os.path.dirname(train_data_path), exist_ok=True)
columns =['Name','Time']
test = []
train = pd.DataFrame(test, columns=columns)
train.to_csv(train_data_path, index=False)

def take_attendance():
    path = 'uploads'
    images = []
    class_names = []
    my_list = os.listdir(path)
    print(my_list)

    for cl in my_list:
        cur_image = cv2.imread(f'{path}/{cl}')
        images.append(cur_image)
        class_names.append(os.path.splitext(cl)[0])
    print(class_names)


    def find_encodings(images):
        encode_list = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)
        return encode_list

    def mark_attendance(name):
        with open('artifacts/attendance.csv','r+') as f:
            my_data_list = f.readlines()
            name_list = []
            for line in my_data_list:
                entry = line.split(',')
                name_list.append(entry[0])

            if name not in name_list:
                now = datetime.now()
                dt_string = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name}, {dt_string}')




    encode_list_known = find_encodings(images)
    print("Encoding complete")

    cap = cv2.VideoCapture(0)

    web=True
    while web:
        success, img = cap.read()
        img_s = cv2.resize(img, (0,0), None, 0.25,0.25)
        img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)

        faces_cur_frame = face_recognition.face_locations(img_s)
        encode_cur_frame = face_recognition.face_encodings(img_s, faces_cur_frame)

        for encode_face, face_loc in zip(encode_cur_frame, faces_cur_frame):
            matches = face_recognition.compare_faces(encode_list_known, encode_face)
            face_dis = face_recognition.face_distance(encode_list_known, encode_face)
            print(face_dis)
            match_index = np.argmin(face_dis)

            if matches[match_index]:
                name = class_names[match_index].upper()
                print(name)
                y1,x2,y2,x1 = face_loc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img, (x1,y2-35),(x2,y2),(0,255,0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                mark_attendance(name)

        cv2.imshow('Webcam',img)
        cv2.waitKey(1)
        if keyboard.is_pressed('q'): 
            web=False # if key 'q' is pressed 
            cv2.destroyAllWindows() 


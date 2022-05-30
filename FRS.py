# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import time

import cv2
import numpy as np
import face_recognition
from tkinter import *
from PIL import Image, ImageTk
import datetime
from datetime import datetime


#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
#    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if _name_ == '_main_':

    path = "Images"
    images = []
    classNames = []
    mylist = os.listdir(path)
    print(mylist)

    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)


    # print(images)

    def findEncodinss(images):
        encodeList = []
        for img in images:

            img1 = cv2.resize(img, (600, 600), interpolation=cv2.INTER_AREA)
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            print("check\n", img1)
            try:
                encode = face_recognition.face_encodings(img1)[0]
                encodeList.append(encode)
            except:
                print(" ")

        return encodeList


    encodeListKnown = findEncodinss(images)
    # print("encoding complete")

    def markAttendance(name):
        with open('Attendence.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')


    def window():
        win = Toplevel(root)
        win.geometry("1080x720")
        win.configure(bg="white")
        Label(win, text="Attendance Cam", font=("times new roman", 30, "bold"), bg="white", fg="black").pack()

        f1 = LabelFrame(win, bg="red")
        f1.pack()
        L1 = Label(f1, bg="red")
        L1.pack()

        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            img1 = cv2.resize(img, (40, 40), None, 0.25, 0.25)
            img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            faceCurFrame = face_recognition.face_locations(img1)
            encodeCurFrame = face_recognition.face_encodings(img1, faceCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    # print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4    # <-- ismen scaling ka msla ha
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)

            cv2.imshow('Webcam', img)
            cv2.waitKey(1)

            img = ImageTk.PhotoImage(Image.fromarray(img1))
            L1['image'] = img

            win.update()

        cap.release()


    root = Tk()
    root.geometry("950x170")
    Label(root, text="Welcome To Face Recognition Attendance System", font=("times new roman", 30, "bold"),
          fg="black").pack(pady=20)
    Button(root, text="Attendance", font=("times new roman", 20, "bold"), bg="white", fg="black", command=window).pack()

    root.mainloop()

import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle

path='C:/Users/Asus/Desktop/IMAGES'

images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
  encodeList = []
  for img in images:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    encodeList.append(encode)
  return encodeList


def markAttendance(name):
  with open('C:/Users/Asus/Desktop/Attendence.csv','r+') as f:
    myDataList = f.readlines()
    nameList = []
    for line in myDataList:
      entry = line.split(',')
      nameList.append(entry[0])
    if name not in nameList:
      now = datetime.now()
      time = now.strftime('%I:%M:%S:%p')
      date = now.strftime('%d-%B-%Y')
      f.writelines(f'\n{name}, {time}, {date}')


encodeListKnown = findEncodings(images)
print('Encoding Complete')


cap = cv2.VideoCapture(0)

while True:
  success, img = cap.read()
  if not success:
    break

  facesCurFrame = face_recognition.face_locations(img)
  encodesCurFrame = face_recognition.face_encodings(img,facesCurFrame)

  for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
    matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
    faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
    #print(faceDis)
    matchIndex = np.argmin(faceDis)

    if matches[matchIndex]:
      name = classNames[matchIndex].upper()
      #print(name)
      y1,x2,y2,x1 = faceLoc
      y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
      cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
      cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
      cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
      markAttendance(name)

  cv2.imshow('Webcam',img)
  cv2.waitKey(1)
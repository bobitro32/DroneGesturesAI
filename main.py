import cv2 as cv
import mediapipe as mp
import time
import HadnTrackingModule as htm
import numpy as np

import math




cap = cv.VideoCapture(0)
detector = htm.HandDetector(minDetectionConf=0.7,maxHands=2)
commands = ["Stay","Up","Down","Right","Left","Forward","Come back"]
index=0
while True:
    success, img = cap.read()
    img =cv.flip(img,2)
    hands, img = detector.findHands(img)

    if hands:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        bbox = hand1["bbox"]

        handType1 = hand1["type"]
        if(handType1 =="Right"):
            if (fingers1 == [0,1,1,1,1]):
                index =0
                cv.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (0, 0, 220), 2)
                cv.putText(img, commands[index], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_PLAIN,
                           2, (0, 0, 0), 2)


                #stay
            elif (fingers1 ==[1,1,0,0,0]):
                index =1
                cv.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                             (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),(106, 0, 255), 2)
                #up
                cv.putText(img, commands[index], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_PLAIN,
                           2, (0, 0, 0), 2)
            elif (fingers1 ==[1,1,1,0,0,]):
                #down
                index = 2
                cv.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                             (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20), (244, 114, 203), 2)
                cv.putText(img, commands[index], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_PLAIN,
                           2, (0, 0, 0), 2)

            elif (fingers1 == [1,0,0,0,1]):
                #right
                index = 3
                cv.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                             (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20), (130, 90, 44), 2)
                cv.putText(img, commands[index], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_PLAIN,
                           2, (0, 0, 0), 2)
            elif (fingers1 == [0,0,0,0,0]):
                #left
                index =4
                cv.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                             (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20), (188,143,143), 2)
                cv.putText(img, commands[index], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_PLAIN,
                           2, (0, 0, 0), 2)
            elif(fingers1 ==[0,1,1,0,0,]):
                #forward
                index = 5
                cv.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                             (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20), (0, 250, 154), 2)
                cv.putText(img, commands[index], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_PLAIN,
                           2, (0, 0, 0), 2)
            elif(fingers1 == [0,1,0,0,0]):
                #Come back
                index = 6
                cv.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                             (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20), (255,255,255), 2)
                cv.putText(img, commands[index], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_PLAIN,
                           2, (0, 0, 0), 2)





    cv.imshow("Handtracker", img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
import cv2 as cv
import mediapipe as mp
import time
import HadnTrackingModule as htm
import numpy as np

import math




cap = cv.VideoCapture(0)
detector = htm.HandDetector(minDetectionConf=0.7,maxHands=2)

while True:
    success, img = cap.read()
    img =cv.flip(img,2)
    hands, img = detector.findHands(img)
    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmark points
            bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"



    cv.imshow("Handtracker", img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
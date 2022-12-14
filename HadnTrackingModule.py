import cv2 as cv
import numpy as np
import time
import mediapipe as mp


class HandDetector():
    def __init__(self, mode=False, maxHands=2,complexity =1, minDetectionConf=0.5, trackConf=0.5,max_num_hands =2):
        self.mode = mode
        self.maxHand = maxHands
        self.complexity = complexity
        self.minDetectionConf = minDetectionConf
        self.trackConf = trackConf
        self.max_num_hands = max_num_hands

        self.mp_hand = mp.solutions.hands
        self.hands = self.mp_hand.Hands(mode, self.maxHand, self.complexity,self.minDetectionConf, self.trackConf)
        self.mp_draw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=False):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                ## lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                ## bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                ## draw
                if not draw:
                    self.mp_draw.draw_landmarks(img, handLms,
                                               self.mp_hand.HAND_CONNECTIONS,self.mp_draw.DrawingSpec(color=(0,0,0), thickness=5, circle_radius=2),
            self.mp_draw.DrawingSpec(color=(0,0,150), thickness=4, circle_radius=2))
                    cv.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 20), 2)
                    cv.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv.FONT_HERSHEY_PLAIN,
                                2, (0, 0, 0), 2)
        if draw:
            return allHands, img
        else:
            return allHands

    def fingersUp(self, myHand):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        :return: List of which fingers are up
        """
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = []
            # Thumb
            if myHandType == "Right":
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

def main():

    cap = cv.VideoCapture(0)
    detector = HandDetector(minDetectionConf=0.5, maxHands=2)

    while True:
        success, img = cap.read()
        img = cv.flip(img,2)
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


if __name__ == "__main__":
    main()


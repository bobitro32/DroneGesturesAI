import cv2 as cv
import numpy as np
import time
import mediapipe as mp


class HandDetector():
    def __init__(self, mode=False, maxHands=2,complexity =1, minDetectionConf=0.5, trackConf=0.5):
        self.mode = mode
        self.maxHand = maxHands
        self.complexity = complexity
        self.minDetectionConf = minDetectionConf
        self.trackConf = trackConf

        self.mp_hand = mp.solutions.hands
        self.hands = self.mp_hand.Hands(mode, self.maxHand, self.complexity,self.minDetectionConf, self.trackConf)
        self.mp_draw = mp.solutions.drawing_utils

    def findHand(self, img, draw=True):
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(img)

        if self.result.multi_hand_landmarks:
            for hand_marks in self.result.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_marks, self.mp_hand.HAND_CONNECTIONS,
                                                self.mp_draw.DrawingSpec(color=(255,0,0),thickness=6),self.mp_draw.DrawingSpec(color=(0,0,0), thickness=8))
        return img
    def findPosition(self,img,handNo=0,draw = True):
            lmList = []

            if self.result.multi_hand_landmarks:
                myHand = self.result.multi_hand_landmarks[handNo]# gives us the hand we want
                #in that hand will give us all the landmarks
                for id, ln in enumerate(myHand.landmark):

                    h, w, c = img.shape
                    cx, cy = int(ln.x * w), int(ln.y * h)  # gives us the position of our hands
                    lmList.append([id,cx,cy])#append the landmarks of the hand, so we can access later certain finger or fingers
                    if draw:
                        cv.circle(img,(cx,cy),8,(20,0,255),cv.FILLED)
            return lmList


def main():
    pTime = 0
    cap = cv.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.findHand(img)
        lmList = detector.findPosition(img)
        if(len(lmList) !=0):
            print(lmList[8])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        img = cv.cvtColor(cv.flip(img, 1), cv.COLOR_BGR2RGB)
        cv.putText(img, f"FPS: {int(fps)}", (40, 70), cv.FONT_HERSHEY_COMPLEX, 3, (0, 0, 250), 3)

        cv.imshow("Handtracker", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()

import cv2
import mediapipe as mp


class handDetector1():
    def __init__(self, mode=False, maxhands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.max_hands = maxhands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mp_drawing = mp.solutions.drawing_utils


    def drawHands(self, img, draw=True):
        #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)
        return

    def circle(self, img, lmLst, draw = True):
        if draw == True:
            cv2.circle(img, lmLst, 20, (0, 0, 255), cv2.FILLED)

    def findPosition_left(self, img, w):
        if self.results.multi_hand_landmarks:
            for myHand1 in self.results.multi_hand_landmarks:
                for id1, lm1 in enumerate(myHand1.landmark):
                    h1, w1, c1 = img.shape
                    cx1, cy1 = int(lm1.x * w1), int(lm1.y * h1)
                    if id1 == 9:
                        if cx1 >= w / 2:
                            lmLst1 = (cx1, cy1)
                            cv2.circle(img, lmLst1, 20, (0, 0, 255), cv2.FILLED)
                            return lmLst1
                        else:
                            return None



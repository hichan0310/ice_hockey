import cv2
import mediapipe as mp


class handDetector2():
    def __init__(self, mode=False, maxhands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.max_hands = maxhands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mp_drawing = mp.solutions.drawing_utils

    def drawHands(self, img, w=640, draw=True):
        # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h1, w1, c1 = img.shape
        self.results = self.hands.process(img)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)
                cx1, cy1, i = 0, 0, 0
                for id1, lm1 in enumerate(handLms.landmark):
                    cx1 += lm1.x
                    cy1 += lm1.y
                    i += 1
                cx1 /= i
                cy1 /= i
                if cx1 <= w / 2:  # 프레임 왼쪽
                    lmLst2 = (int(cx1 * w1), int(cy1 * h1))
                    cv2.circle(img, lmLst2, 20, (0, 255, 0), cv2.FILLED)
                    return lmLst2
                else:
                    return None

    def circle(self, img, lmLst, draw=True):
        if draw == True:
            cv2.circle(img, lmLst, 20, (0, 255, 0), cv2.FILLED)

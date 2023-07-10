import cv2
import numpy as np
import mediapipe as mp
import pyautogui as pg
from settings import *


class Camera:
    def __init__(self, mode):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.face_detection = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        self.mode=mode

    def get_pos(self):
        File = open("test.txt", "r")
        text = File.read()
        File.close()
        try:a,b,c,d=map(lambda x:int(float(x)), text.split(',')[:4])
        except:return
        return (a*SCREEN_WIDTH/640,b*SCREEN_HEIGHT/480) if self.mode==0 else (c*SCREEN_WIDTH/640,d*SCREEN_HEIGHT/480)

    def delete(self):
        self.cap.release()
        self.face_detection.close()
        cv2.destroyAllWindows()

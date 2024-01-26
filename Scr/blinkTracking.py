import cv2
import numpy as np
import dlib
from math import hypot
import statistics
import os

class BlinkTracking():
    def __init__(self):
        self.blinkd = False
        self.blinkcount = 0
        self.blockcount = False
        self.cap =cv2.VideoCapture(0)


        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(os.path.dirname(__file__) + "\\shape_predictor_68_face_landmarks.dat")
        self.font = cv2.FONT_ITALIC
        self.openEyeMean = 3
        self.openEyeList = [5]
        self.tickcount = 0
        self.openEyeSD = 3
        self.openEyeCurrent = 1
        self.oldBlink = 0
        self.shouldUpdate = 5

    def eyenblink(self,a,b,c,d,e,f, landmarks):

        left_point = (landmarks.part(a).x, landmarks.part(a).y)
        right_point = (landmarks.part(d).x, landmarks.part(d).y)

        center_top = self.midpoint(landmarks.part(b), landmarks.part(c))
        center_bottom = self.midpoint(landmarks.part(f), landmarks.part(e))

        hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_length = hypot((center_top[0] - center_bottom[0]), center_top[1] - center_bottom[1])
        if hor_line_length > 0 and ver_line_length > 0:

            ratio = hor_line_length / ver_line_length
            return ratio
        else:
            return 3
    def midpoint(self,p1,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)
    def update(self):
        if self.shouldUpdate == 5:
            _, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray)
            for face in faces:
                lmarks = self.predictor(gray, face)
                left = self.eyenblink(36,37,38,39,40,41,lmarks)
                right = self.eyenblink(45, 44, 43, 42, 47, 46,lmarks)

                self.openEyeCurrent = (left + right) / 2

                if ((left + right) / 2 > (self.openEyeSD* 3 ) + self.openEyeMean and not self.blockcount):
                    self.blinkcount += 1
                    self.framesSinceLast = 0

                    self.blinkd = True

                    self.blockcount = True


                elif (left + right) / 2 < self.openEyeMean + self.openEyeSD * 1.5:


                    if len(self.openEyeList) + 1 < 1000:
                        self.openEyeList.append((left + right) / 2)

                        self.openEyeMean = statistics.fmean(self.openEyeList)
                        self.openEyeSD = statistics.pstdev(self.openEyeList)


                    self.blockcount = False
                    self.blinkd = False
                else:
                    self.blinkd = False
            self.shouldUpdate = 1
        else:
            self.shouldUpdate += 1




    def blinked(self):
        return self.blinkd



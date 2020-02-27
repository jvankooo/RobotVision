import cv2
import numpy as np
import pickle

#Main

cam = cv2.VideoCapture(0)

#load homography data
f = open("calibration.txt", "rb")
try:
	h = pickle.load(f)
except:
	input("Calibration Required, Press enter when ready")
	h = CalibratePrespective()
f.close()


cam = cv2.VideoCapture(0)

cal_frame = cv2.warpPerspective(frame, h, (frame.shape[1], frame.shape[0]))
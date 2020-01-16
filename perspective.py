import cv2
import numpy as np
import pickle

chess_w, chess_h = 4, 7

# Store the calibration data
def store_data(data):

	f = open("calibration.txt", "wb")
	pickle.dump(data, f)
	f.close()


#Calculate and return homography matrix
def CalibratePrespective():

	print("Calibrating Camera...")

	ret, frame = cam.read()
	ref = cv2.imread('calb.jpg')

	ret1, corners1 = cv2.findChessboardCorners(ref, (chess_h,chess_w), None)
	ret2, corners2 = cv2.findChessboardCorners(frame, (chess_h,chess_w), None)

	if ret2 == True:
		h_mat, status = cv2.findHomography(corners2, corners1)
		ref = cv2.drawChessboardCorners(ref, (7,4), corners1,ret1)
		frame = cv2.drawChessboardCorners(frame, (7,4), corners2,ret2)
		pt1, pt2, pt3, pt4 = repr(corners2[0]), tuple(corners2[chess_h-1]), tuple(corners2[chess_h*chess_w-1]), tuple(corners2[chess_h*chess_w-chess_h-1])
		print(pt1, pt2, pt3, pt4)
		# cv2.line(frame, pt1[0], pt2[0], (0, 0, 255), 2)
		# cv2.line(frame, tuple(corners2[chess_h-1]), tuple(corners2[chess_h*chess_w-1]), (0, 0, 255), 2)
		# cv2.line(frame, tuple(corners2[chess_h*chess_w-1]), tuple(corners2[chess_h*chess_w-chess_h-1]), (0, 0, 255), 2)
		# cv2.line(frame, tuple(corners2[chess_h*chess_w-chess_h-1]), tuple(corners2[0]), (0, 0, 255), 2)
		cv2.imshow('result', frame)
		cv2.waitKey(0)
		cv2.destroyWindow('result')
		print(" Camera Calibrated ", h_mat)
		store_data(h_mat)
		return h_mat
	else:
		raise Exception("Chessboard not found")




#Main

cam = cv2.VideoCapture(0)

#load calibration data
f = open("calibration.txt", "rb")
try:
	h = pickle.load(f)
except:
	input("Calibration Required, Press enter when ready")
	h = CalibratePrespective()
f.close()


# Main Loop
while(True):

	ret, frame = cam.read()
	# Apply Prespective Transform

	cal_frame = cv2.warpPerspective(frame, h, (frame.shape[1], frame.shape[0]))

	# Re-Calibration
	if cv2.waitKey(1) & 0xFF == ord('c'):
		# try:
		# 	h_old = h
		# 	h = CalibratePrespective()
		# except:
		# 	h = h_old
		# 	print("Calibration Failed")
		# 	continue
		h_old = h
		h = CalibratePrespective()

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	#Processing


	# Display Window
	cv2.imshow('frame',cal_frame)



cam.release()
cv2.destroyAllWindows()



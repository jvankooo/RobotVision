import cv2
import numpy as np
import pickle

# chessboard size
chess_w, chess_h = 4, 7

# Store the homography data
def store_data(data):

	f = open("perspective.pickle", "wb")
	pickle.dump(data, f)
	f.close()


#Calculate and return homography matrix
def CalibratePrespective():

	print("Calculating Homogrphy Matrix...")

	ret, frame = cam.read()

	# load the reference image
	ref = cv2.imread('img/reference.jpg')

	# find the chessboard corners
	ret1, corners1 = cv2.findChessboardCorners(ref, (chess_h,chess_w), None)
	ret2, corners2 = cv2.findChessboardCorners(frame, (chess_h,chess_w), None)

	# check if corners exist
	if ret2 == True:

		# Calculate homogrphy transform matrix
		h_mat, status = cv2.findHomography(corners2, corners1)

		frame = cv2.drawChessboardCorners(frame, (chess_h,chess_w), corners2,ret2)

		cv2.imshow('result', frame)
		cv2.waitKey(0)

		# apply the perspective correction on the frame
		transformed_frame = cv2.warpPerspective(frame, h_mat, (frame.shape[1], frame.shape[0]))

		cv2.imshow('result', transformed_frame)
		cv2.waitKey(0)

		cv2.destroyWindow('result')
		print(" Calculated Matrix ", h_mat)

		store_data(h_mat)

	else:
		raise Exception("Chessboard not found")




#Main

cam = cv2.VideoCapture(0)

# Main Loop
while(True):

	ret, frame = cam.read()

	# cal_frame = cv2.warpPerspective(frame, h, (frame.shape[1], frame.shape[0]))

	k = cv2.waitKey(1)

	# Re-Calibration
	if k == ord('c'):
		# try:
		# 	CalibratePrespective()
		# except:
		# 	print("Chessboard not found. Try Again : Press c")
		# 	continue
		CalibratePrespective()

	if k == ord('q'):
		break


	# Display Window
	cv2.imshow('frame',frame)



cam.release()
cv2.destroyAllWindows()



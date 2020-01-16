import numpy as np
import cv2
import pickle

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*4,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:4].T.reshape(-1,2)

objpoints.append(objp)

img = cv2.imread('img/uncalibrated.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #convert to grayscale

# Find the chessboard corners
found, corners = cv2.findChessboardCorners(gray, (7,4),None)

# If found, add object points, image points (after refining them)
if found == True:
    corners_refined = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))

    imgpoints.append(corners_refined)

    # Draw and display the corners
    img_corners = cv2.drawChessboardCorners(img, (7,4), corners_refined, found)
    cv2.imshow('corners',img_corners)
    cv2.waitKey(0)

# find distortion coefficients
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1:],None,None)

# undistort
calibrated = cv2.undistort(img, mtx, dist, None, mtx)

cv2.imshow('calibrated',calibrated)
cv2.waitKey(0)
cv2.destroyAllWindows()

# store the data
f = open('calibrated.pickle', 'wb')
pickle.dump([dist, mtx], f)
f.close()
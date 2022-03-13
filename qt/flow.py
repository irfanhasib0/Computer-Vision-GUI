import numpy as np
import cv2 as cv
import argparse

class OpticalFlow():
    def __init__(self):
        self.feature_params = dict( maxCorners = 100,
		               qualityLevel = 0.3,
		               minDistance = 7,
		               blockSize = 7 )

        self.lk_params = dict( winSize  = (15, 15),
		          maxLevel = 2,
		          criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

        self.color = np.random.randint(0, 255, (100, 3))
        self.old_frame = 0
        self.p0 = 0
	
    def get_flow(self,frame):
        if type(self.old_frame) == int:
           self.old_frame = frame
           old_gray = cv.cvtColor(self.old_frame, cv.COLOR_BGR2GRAY)
           self.p0 = cv.goodFeaturesToTrack(old_gray, mask = None, **self.feature_params)
           return frame, frame
           
        old_gray = cv.cvtColor(self.old_frame, cv.COLOR_BGR2GRAY)
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        p0 = cv.goodFeaturesToTrack(old_gray, mask = None, **self.feature_params)

	# Create a mask image for drawing purposes
        mask = np.zeros_like(self.old_frame)

	# calculate optical flow
        p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **self.lk_params)
        
        hsv = np.zeros_like(frame)
        hsv[..., 1] = 255
        flow = cv.calcOpticalFlowFarneback(old_gray, frame_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang*180/np.pi/2
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        #cv.imshow('frame2', bgr)
    
	# Select good points
        if p1 is not None:
            good_new = p1[st==1]
            good_old = p0[st==1]
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)),  self.color[i].tolist(), 2)
            frame = cv.circle(frame, (int(a), int(b)), 5, self.color[i].tolist(), -1)
	    
        img = cv.add(frame, mask)
        self.old_gray = frame_gray.copy()
        self.p0 = good_new.reshape(-1, 1, 2)
        return img ,bgr

import numpy as np
import imutils
import cv2
import sys
import skvideo.io

cap = skvideo.io.VideoCapture('http://192.168.0.33:81/videostream.cgi?loginuse=admin&loginpas=888888')

# Define the codec and create VideoWriter object
#fourcc = cv2.CV_FOURCC(*'XVID')
#out = cv2.VideoWriter('/home/azureuser/Project/output.avi',fourcc, 20.0, (1280, 720))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #frame = imutils.resize(frame, width=640, height=480)
        #frame = cv2.flip(frame,-1)

        # write the flipped frame
        #out.write(frame)
        print("Frame writing")
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
#out.release()
cv2.destroyAllWindows()
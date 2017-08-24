# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
import argparse
from datetime import datetime, timedelta
import imutils
import time
import datetime
import cv2
import StopWatch
import uuid
import requests
import json
from azure.storage.blob import BlobService
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ag", "--ag", default='7ce76956-b9bd-4f5d-b23b-6a33ce174dd4', help="aggregator id")
ap.add_argument("-ip", "--ip", default='http://192.168.0.15/', help="aggregator ip")
ap.add_argument("-c", "--camera", default='1494b7be-4233-4096-bf8d-8470f7783633', help="camera id")
ap.add_argument("-cu", "--cu", default='1494b7be-4233-4096-bf8d-8470f7783633', help="camera id")
args = vars(ap.parse_args())
blobService = BlobService(account_name='chango', account_key='h/RbA/QMVr9lyndGvaPIw3A1uugvui+RJHM5e4lOrly6/fBM2N79RW/Svbz3Rdx+rulIyWJB80f1BvmlZjXOfg==')
path = '/home/Videos/' + args["ag"] + '/' + args["camera"] + '/'
imagepath = '/home/Images/' + args["ag"] + '/' + args["camera"] + '/'
#argsvideo = 'http://52.187.67.18/live/' + args["ag"] + '^' + args["camera"] + '/index.m3u8'
argsvideo = args["cu"]
argsmin_area = 500
IsMotionfound = False
ShouldServiceCalled = True

def SaveVideo(start_date,filename):
    url = 'http://8edd9ae4f6214bab91d2d65c64b23d05.cloudapp.net/api/CameraVideoOnDemand/AddVideoOnDemand'
    end_date = start_date + timedelta(seconds=30)
    videoUrl = args["ip"] + 'Videos/' + args["ag"] + '/' + args["camera"] + '/' + filename + ".avi"
    imageUrl = 'https://chango.blob.core.windows.net/analyticimage/' + filename + ".png"
    data = {"AgreegatorId": args["ag"], "CameraId": args["camera"], "end_date":end_date,"start_date":start_date,"text":videoUrl,"media":imageUrl}
    response = requests.post(url, data=data)
    response.status_code
    response.text

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(argsvideo)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(argsvideo)

(grabbed, frame) = camera.read()
height, width, channels = frame.shape

timenow = datetime.datetime.now()
filename = str(timenow.strftime("%Y%m%d%H%M%S"))
SaveVideo(timenow,filename)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
#out = cv2.VideoWriter(path + str(uuid.uuid4()) + '.avi' ,fourcc, 20.0, (width,
#height))
cv2.imwrite(imagepath + filename + '.png', frame)
blobService.put_block_blob_from_path("analyticimage", filename + '.png', imagepath + filename + '.png')
out = cv2.VideoWriter(path + filename + '.avi' ,fourcc, 20.0, (width, height))
# initialize the first frame in the video stream
firstFrame = None
motionStartWatch = StopWatch.Timer()
motionStopWatch = StopWatch.Timer()
motionStartWatch.start()
motionStopWatch.start()

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "Unoccupied"


        writerFrame = frame

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)


	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < argsmin_area:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

        if text == "Occupied": 
            IsMotionfound = True 
            motionStopWatch.restart() 
        else:
            if motionStopWatch.time_elapsed >= 10 and IsMotionfound:
                IsMotionfound = False
                timenow = datetime.datetime.now()
                filename = str(timenow.strftime("%Y%m%d%H%M%S"))
                SaveVideo(timenow,filename)
                cv2.imwrite(imagepath + filename + '.png', writerFrame)
                blobService.put_block_blob_from_path("analyticimage", filename + '.png', imagepath + filename + '.png')
                out = cv2.VideoWriter(path + filename + '.avi' ,fourcc, 20.0, (width, height))
                motionStartWatch.restart()
                motionStopWatch.restart()
                ShouldServiceCalled = True
            else:
                motionStopWatch.restart()

        if IsMotionfound and motionStartWatch.time_elapsed >= 2:
            out.write(writerFrame)
        if IsMotionfound and motionStartWatch.time_elapsed >= 30:
            timenow = datetime.datetime.now()
            filename = str(timenow.strftime("%Y%m%d%H%M%S"))
            SaveVideo(timenow,filename)
            cv2.imwrite(imagepath + filename + '.png', writerFrame)
            blobService.put_block_blob_from_path("analyticimage", filename + '.png', imagepath + filename + '.png')
            out = cv2.VideoWriter(path + filename + '.avi' ,fourcc, 20.0, (width, height))
            motionStartWatch.restart() 
        if ShouldServiceCalled and IsMotionfound:
                requ = requests.post('http://8edd9ae4f6214bab91d2d65c64b23d05.cloudapp.net/api/CloudMessageController/InvokeCamera?guidCamera=' + args["camera"])
                print("analytic called")
                ShouldServiceCalled = False
	# draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        print(text)

	# show the frame and record if the user presses a key
	#cv2.imshow("Security Feed", frame)
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
out.release()
cv2.destroyAllWindows()


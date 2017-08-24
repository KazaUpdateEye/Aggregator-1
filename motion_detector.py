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
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("-ag", "--ag", default='7ce76956-b9bd-4f5d-b23b-6a33ce174dd4', help="aggregator id")
ap.add_argument("-ip", "--ip", default='http://192.168.0.15/', help="aggregator ip")
ap.add_argument("-c", "--camera", default='1494b7be-4233-4096-bf8d-8470f7783633', help="camera id")
ap.add_argument("-st", "--storage", default='hybrid', help="storage type")
ap.add_argument("-f", "--framerate", default='15', help="frame rate")
ap.add_argument("-r", "--resolution", default='640x480', help="resolution")
args = vars(ap.parse_args())


if (args["storage"] == 'Hybrid' or args["storage"] == 'Cloud'):
	args["storage"] = 'Hybrid'
	path = '/home/Videos/' + args["ag"] + '/' + args["camera"] + '/' + args["storage"] + '/'
	print(path)
else:
	path = '/home/Videos/' + args["ag"] + '/' + args["camera"] + '/'

imagepath = '/home/Images/' + args["ag"] + '/' + args["camera"] + '/'
argsvideo = 'rtmp://localhost/live/' + args["ag"] + '^' + args["camera"]

videoDuration = 10
argsmin_area = 200
DoRecoding = False
fps = 10
ShouldServiceCalled = False
IsServiceCalled = False
timenow = datetime.datetime.now()
filename = str(uuid.uuid4())
fourcc = cv2.cv.CV_FOURCC(*'XVID')
FirstImage = None
LastImage = None
# initialize the first frame in the video stream
firstFrame = None
motionStartWatch = StopWatch.Timer()
motionStopWatch = StopWatch.Timer()

#dump json data into file
def SaveVideo(start_date,filename,imgpath):
    end_date = start_date + timedelta(seconds=videoDuration)
    videoUrl = args["ip"] + 'Videos/' + args["ag"] + '/' + args["camera"] + '/' + args["storage"] + '/' + filename + ".avi"
    LastimageUrl = 'https://changovideoanalytics.blob.core.windows.net/analyticimage/' + filename + "_Last.png"
    FirstImageUrl = 'https://changovideoanalytics.blob.core.windows.net/analyticimage/' + filename + "_First.png"
    data = {"AgreegatorId": args["ag"], "CameraId": args["camera"], "end_date":str(end_date),"start_date":str(start_date),"text":videoUrl,"media":FirstImageUrl,"LocalImageFirst":imgpath + filename + '_First.png',"EndThumbnailUrl":LastimageUrl,"LocalImageLast":imgpath + filename + '_Last.png'}
    with open('/home/project/DumpJson/' + filename + '.json', 'w') as outfile:
        json.dump(data, outfile)
#Test Local
#SaveVideo(timenow,filename,'')
if args.get("video", None) is None:
	camera = cv2.VideoCapture(argsvideo)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(argsvideo)

(grabbed, frame) = camera.read()
resizedframe = imutils.resize(frame, width=240)
height, width, channels = resizedframe.shape
motionStopWatch.start()
motionStartWatch.start()
while True:
    (grabbed, frame) = camera.read()
    text = "Unoccupied"
    writeFrame = frame
    #if the frame could not be grabbed, then we have reached the end
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
    # compute the absolute difference between the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    firstFrame = gray
    # dilate the thresholded image to fill in holes, then find contours on
    # thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < argsmin_area:
            continue
        # compute the bounding box for the contour, draw it on the frame, and
        # update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    #print(motionStartWatch.time_elapsed)
    if text == "Occupied":           
        ShouldServiceCalled = True
        DoRecoding = True
        motionStopWatch.restart()
    if ShouldServiceCalled and IsServiceCalled == False:        
        print('First Image Capture')
        with open("/home/Aggregator/PlayLive.txt", mode='w') as file:
            file.write('%s' %(datetime.datetime.now()))
        #rc = subprocess.call("/home/Aggregator/onMotionHls.sh " + args['ag'] + " " + args['camera'] + " " + args['framerate'] + " " + args['resolution'], shell=True) 
        filename = str(uuid.uuid4())
        out = cv2.VideoWriter(path + filename + '.avi' ,fourcc, fps, (width, height),True)
        IsServiceCalled = True
        imgpathFirst = imagepath + filename + '_First.png'
        resizedimage = imutils.resize(writeFrame, width=240)
        cv2.imwrite(imgpathFirst, resizedimage)
        #requ = requests.post('http://0f8202c8526b4c35aae76a654dd1e0a1.cloudapp.net/api/CloudMessageController/InvokeCamera?guidCamera=' + args["camera"])
    if text == "Unoccupied" and motionStopWatch.time_elapsed > 2 and DoRecoding:
        print('Saving Video motionStopWatch' + str(motionStopWatch.time_elapsed))
        timenow = datetime.datetime.now()
        imgpathLast = imagepath + filename + '_Last.png'
        resizedimage = imutils.resize(writeFrame, width=240)
        cv2.imwrite(imgpathLast, resizedimage)
        motionStartWatch.restart() 
        ShouldServiceCalled = False
        IsServiceCalled = False
        DoRecoding = False
        SaveVideo(timenow,filename,imagepath)
        filename = str(uuid.uuid4())
    if DoRecoding:
        print('Adding Frame')
        resizedimage = imutils.resize(writeFrame, width=240)
        out.write(resizedimage)
    
    if motionStartWatch.time_elapsed >= videoDuration:
        print('Saving Video motionStartWatch' + str(motionStartWatch.time_elapsed))
        timenow = datetime.datetime.now()
        imgpathLast = imagepath + filename + '_Last.png'
        resizedimage = imutils.resize(writeFrame, width=240)
        cv2.imwrite(imgpathLast, resizedimage)
        motionStartWatch.restart() 
        ShouldServiceCalled = False
        IsServiceCalled = False
        DoRecoding = False
        SaveVideo(timenow,filename,imagepath)
        filename = str(uuid.uuid4())
    if DoRecoding == False:
        #rc = subprocess.call("/home/Aggregator/NoMotionHls.sh " + args['ag'] + " " + args['camera'] + " " + args['framerate'] + " " + args['resolution'], shell=True)
        motionStopWatch.restart()
        motionStartWatch.restart() 
    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    print(text)
    # show the frame and record if the user presses a key
    #cv2.imshow("Security Feed", frame)
    #cv2.imshow("Thresh", thresh)
    #cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

camera.release()
out.release()
cv2.destroyAllWindows()

#!/usr/bin/env python
import cv2
import sys
import numpy as np

cameraDevice = 0
video_file = "step_"
width = 830/2
height = 540/2
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')

for index in range(1,7):
    read_frame = True
    # camera_capture = cv2.VideoCapture(cameraDevice)
    video_out = cv2.VideoWriter(video_file+str(index)+'_out.avi',fourcc,15,(width,height))
    video_capture = cv2.VideoCapture(video_file+str(index)+".mp4")
    while True:
        # read_camera, img_cam = camera_capture.read()
        read_video, img_video = video_capture.read()
        if img_video is None:
            break;
        # height_cam, width_cam, channels = img_cam.shape

        # is_sucessfuly_read will return false when the a file ends, or is no
        #   longer available, or has never been available
        if(read_video):
            if(read_frame):
                img_resized = cv2.resize(img_video[:,130:960,:],(0,0),fx=0.5,fy=0.5)
                video_out.write(img_resized)
        else:
            print "Cannot read video capture"
            break
        read_frame = not read_frame

        # Necesary wait for full rendering
        cv2.waitKey(30)

    cv2.destroyAllWindows()
    video_out.release()

#!/usr/bin/env python
import cv2
import sys
import numpy as np

cameraDevice = 0
video_file = "new_step"
orig_width = 640
orig_height = 360
scaling_factor = 1.5
width = int(orig_width/scaling_factor)
height = int(orig_height/scaling_factor)
height_sub = int(70/scaling_factor)
width_sub = 0
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
black = np.zeros((orig_height,orig_width,3), np.uint8)

for index in range(1,8):
    print "vid: ", index
    read_frame = True
    video_out = cv2.VideoWriter(video_file+str(index)+'_out.avi',fourcc,15,(width-width_sub,height-height_sub))
    video_capture = cv2.VideoCapture(video_file+str(index)+".mov")
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
                mask = np.logical_and(img_video[:,:,0] <=29, img_video[:,:,1] <=32, img_video[:,:,2] <=0)
                img_video[:,:,0] = np.multiply(img_video[:,:,0], np.logical_not(mask).astype(int)) +\
                        np.multiply(black[:,:,0], mask.astype(int))
                img_video[:,:,1] = np.multiply(img_video[:,:,1], np.logical_not(mask).astype(int)) +\
                        np.multiply(black[:,:,1], mask.astype(int))
                img_video[:,:,2] = np.multiply(img_video[:,:,2], np.logical_not(mask).astype(int)) +\
                        np.multiply(black[:,:,2], mask.astype(int))
                img_resized = cv2.resize(img_video,(width,height))
                img_cropped = img_resized[height_sub:height,0:width-width_sub,:]
                video_out.write(img_cropped)
        else:
            print "Cannot read video capture"
            break
        read_frame = not read_frame

        # Necesary wait for full rendering
        cv2.waitKey(30)

    cv2.destroyAllWindows()
    video_out.release()

#!/usr/bin/env python
import cv2
import sys
import numpy as np

cameraDevice = 0
alpha = 1
EDGES = False
video_file = "new_step"

camera_capture = cv2.VideoCapture(cameraDevice)

for index in range(1,8):
    video_capture = cv2.VideoCapture(video_file+str(index)+'_out.avi')
    while True :
        read_camera, img_cam = camera_capture.read()
        read_video, img_video = video_capture.read()
        if img_cam is None or img_video is None:
            break;
        height_cam, width_cam, channels = img_cam.shape
        height_vid, width_vid, channels = img_video.shape
        offset_row = (height_cam - height_vid)/2
        offset_col = (width_cam - width_vid)/2
        # Create the overlay image
        overlay = img_cam.copy()
        output = img_cam.copy()

        # is_sucessfuly_read will return false when the a file ends, or is no
        #   longer available, or has never been available
        if(read_camera and read_video):
            # Overlap images
            mask =np.logical_and(img_video[:,:,0]==0, img_video[:,:,1] ==0, img_video[:,:,2]==0)
            if EDGES:
                img_video = cv2.Canny(img_video,50,100)
            overlay[offset_row:offset_row+height_vid, offset_col:offset_col+width_vid] = img_video
            background = img_cam[offset_row:offset_row+height_vid, offset_col:offset_col+width_vid,:]
            # Eliminate black background
            overlay[offset_row:offset_row+height_vid, offset_col:offset_col+width_vid,0] = np.multiply(background[:,:,0], mask.astype(int)) +\
                    np.multiply(img_video[:,:,0], np.logical_not(mask).astype(int))
            overlay[offset_row:offset_row+height_vid, offset_col:offset_col+width_vid,1] = np.multiply(background[:,:,1], mask.astype(int)) +\
                    np.multiply(img_video[:,:,1], np.logical_not(mask).astype(int))
            overlay[offset_row:offset_row+height_vid, offset_col:offset_col+width_vid,2] = np.multiply(background[:,:,2], mask.astype(int)) +\
                    np.multiply(img_video[:,:,2], np.logical_not(mask).astype(int))
            # overlay[offset_row:offset_row+height_vid, offset_col:offset_col+width_vid,3] = mask.astype(int)*255

            cv2.addWeighted(overlay, alpha, output, 1-alpha,  0, output)
            cv2.imshow("Camera Feed", output)
        else:
            print "Cannot read video capture"
            break

        # Necesary wait for full rendering
        cv2.waitKey(30)

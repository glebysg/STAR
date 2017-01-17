#!/usr/bin/env python
import cv2
import sys
import numpy as np

cameraDevice = 0
alpha = 1
EDGES = False

def skip(arg):
    pass

camera_capture = cv2.VideoCapture(cameraDevice)
for video_file in ["Clean-white"]:#, "step2", "step3", "step4", "step5", "step6", "step7" ]:
    video_capture = cv2.VideoCapture(video_file+".mp4")
    window_name = 'Camera Feed'
    cv2.namedWindow(window_name)
    # Create Trackbars
    cv2.createTrackbar('R',window_name,0,255,skip)
    cv2.createTrackbar('G',window_name,0,255,skip)
    cv2.createTrackbar('B',window_name,0,255,skip)
    cv2.createTrackbar('SwitchR',window_name,0,1,skip)
    cv2.createTrackbar('SwitchG',window_name,0,1,skip)
    cv2.createTrackbar('SwitchB',window_name,0,1,skip)
    while True :
        r = cv2.getTrackbarPos('R', window_name)
        g = cv2.getTrackbarPos('G', window_name)
        b = cv2.getTrackbarPos('B', window_name)
        s_r = cv2.getTrackbarPos('SwitchR', window_name)
        s_g = cv2.getTrackbarPos('SwitchG', window_name)
        s_b = cv2.getTrackbarPos('SwitchB', window_name)
        read_camera, img_cam = camera_capture.read()
        read_video, img_video = video_capture.read()
        if img_cam is None or img_video is None:
            print "b:", b, "g:", g, "r", r
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
            mask =np.logical_and(img_video[:,:,0]>=b if s_r else img_video[:,:,0]<=b,
                    img_video[:,:,1] >=g if s_g else img_video[:,:,0]<=g,
                    img_video[:,:,2]>=r if s_r else img_video[:,:,0]<=r)
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
            cv2.imshow(window_name, output)
        else:
            print "Cannot read video capture"
            break

        # Necesary wait for full rendering
        cv2.waitKey(30)

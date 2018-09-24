#!/usr/bin/env python

# import the AddTwoInts service
from refills_counting_image_saver.srv import *
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError

# rospy for the subscriber
import rospy
# OpenCV2 for saving an image
import cv2
import shutil
# MSG filter for synchronized subs
import message_filters
# Instantiate CvBridge
bridge = CvBridge()
import glob

#Savin the stream from the camera
cv2_img_rs = None
cv2_img_wrist = None

#The actually call when you requestthe server --> saving the pictures
def save_image(req):
    print ("Received a request")
    # Save your OpenCV2 image color  as a png 
    global cv2_img_rs
    # File will be saved with the name: danNumber_realsense.png
    name_realsense = 'dan'+str(req.NameForPicture)+'_realsense'+'.png'
    # On the console a print will appear
    print ('Realsense picture was saved with the name: ' + name_realsense)
    # Picture saved
    cv2.imwrite(name_realsense, cv2_img_rs)

    #same as above just for the flir camera
    global cv2_img_wrist
    name_flir = 'dan'+str(req.NameForPicture)+'_flir'+'.png'
    print ('Flir picture was saved with the name: ' + name_flir)
    cv2.imwrite(name_flir, cv2_img_wrist)
    
    #here we declear source_files and folder. The pictures will be saved localy and then will be moved to the given folder.    
    source_files='*.png'
    target_folder='/home/refills/workspace/rs_ws/src/refills_counting_image_saver/refills_counting_pictures'

    # retrieve file list
    filelist=glob.glob(source_files)
    # move file with full paths as shutil.move() parameters
    for single_file in filelist:   
     shutil.move(single_file,target_folder) 
    #returns the Name--> no need to handle the return value
    return saveImageResponse(req.NameForPicture)

def image_callback(Image_Color_Rs, Image_Color_Wrist):
    try:
        # Convert your ROS Image message to OpenCV2
        global cv2_img_rs
        cv2_img_rs = bridge.imgmsg_to_cv2(Image_Color_Rs, "bgr8")
        global cv2_img_wrist 
        cv2_img_wrist = bridge.imgmsg_to_cv2(Image_Color_Wrist, "bgr8")
    except CvBridgeError, e:
        print(e)
     
def save_image_server():
    print("Server is running waiting for request, pictures will be saved in the folder in which the server was started")
    rospy.init_node('save_image_server')
    s = rospy.Service('saving_image', saveImage, save_image)
    # Define your image topic
    image_topic_rs_camera = "/rs_camera/color/image_raw"
    image_topic_wrist_camera = "/refills_wrist_camera/image_raw"
    # Set up your subscriber and define its callback
    image_rs_sub = message_filters.Subscriber(image_topic_rs_camera, Image)
    image_wrist_sub = message_filters.Subscriber(image_topic_wrist_camera, Image)
    # Callback synchrized
    ts = message_filters.ApproximateTimeSynchronizer([image_rs_sub, image_wrist_sub],100, 10) 
    ts.registerCallback(image_callback)
    # spin() keeps Python from exiting until node is shutdown
    rospy.spin()

if __name__ == "__main__":
    save_image_server()

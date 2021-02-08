#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import message_filters as mf
import os
import numpy as np
from std_msgs.msg import Float32


class topic_subcriber:

    def __init__(self):
        self.video = '/camera/image_color'
        # self.video = mf.Subscriber(video, Image)
        self.video = mf.Subscriber(self.video, Image)
        self.bridge = CvBridge()

    def camera_topic_subscriber(self, video):

        cv2_img = self.bridge.imgmsg_to_cv2(video, "bgr8")
        cv2_img2 = cv2.resize(cv2_img, (1600, 380))
        #shape = cv2_img.shape
        cv2_img3 = cv2_img[400:780,10:1910,:]
        #print(cv2_img3.shape)
        a = np.mean(cv2_img3)
        print(a)
        pub = rospy.Publisher("ref",Float32,queue_size=10)
        pub.publish(a)
        #cv2.imshow('Shrinked', cv2_img)
        #cv2.imshow('ro', cv2_img2)
        cv2.imshow('ro222', cv2_img3)
        cv2.waitKey(1)

    def topic_registration(self):
        time_topic = mf.ApproximateTimeSynchronizer( [self.video], 10, 0.1, allow_headerless=True)
        time_topic.registerCallback(self.camera_topic_subscriber)

if __name__ == "__main__":
    rospy.init_node('camera_topic', anonymous=True)
    topic_sub = topic_subcriber()
    topic_sub.topic_registration()
    rospy.spin()



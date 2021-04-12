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
        cv2_img_test = cv2_img[400:780, 10:1910, :]
        dd = cv2.cvtColor(cv2_img_test,cv2.COLOR_BGR2GRAY)
        a = np.mean(dd)
        print(a)
        pub = rospy.Publisher("ref", Float32, queue_size=1)
        pub.publish(a)
        reshape_img = cv2.resize(cv2_img, (600, 400))
        cv2.imshow('test_img', reshape_img)
        cv2.waitKey(1)

    def topic_registration(self):
        time_topic = mf.ApproximateTimeSynchronizer([self.video], 10, 0.1, allow_headerless=True)
        time_topic.registerCallback(self.camera_topic_subscriber)


if __name__ == "__main__":
    rospy.init_node('camera_topic', anonymous=True)
    topic_sub = topic_subcriber()
    topic_sub.topic_registration()
    rospy.spin()
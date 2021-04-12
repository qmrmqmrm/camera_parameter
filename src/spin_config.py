#!/usr/bin/env python

import rospy
import dynamic_reconfigure.client as dc
import dynamic_reconfigure.server as ds
import numpy as np
from std_msgs.msg import Float32


class CameraDefult:
    exposure = 0
    target_grey_value = 4.0
    framerate = 12
    logexp = 4


class CameraParams:
    exposure = CameraDefult.exposure
    target_grey_value = CameraDefult.target_grey_value
    framerate =CameraDefult.framerate
    logexp = CameraDefult.logexp


class CameraAutoAdjuster:
    def __init__(self):
        self.sub = rospy.Subscriber("ref", Float32, self.ref_callback)
        self.ref = 100
        self.client = dc.Client("/acquisition_node", timeout=100,
                                                        config_callback=self.callback)
        self.target =100
        self.pL = 0.002
        self.pE = 0.0002

    def change_config(self):
        err = self.target - self.ref
        #print(err)
        if err > 10 or err < -10:
            CameraParams.target_grey_value += self.pL * err
            
            CameraParams.target_grey_value = max(min(CameraParams.target_grey_value,90.0),4.0)

            config = {"exposure_time":CameraParams.exposure,
                      "target_grey_value": CameraParams.target_grey_value} # # 
            #print("set config:", config)
            self.client.update_configuration(config)
        config = {"auto_white_balance": True}
        #rospy.loginfo("err:{}".format(err))


    def ref_callback(self, data):
        self.ref = data.data
        #print("ref value:", self.ref)

    def callback(self, config):
        rospy.loginfo("exposure_time :{exposure_time},target_grey_value: {target_grey_value}".format(**config))



def main():
    rospy.init_node("dynamic_client")
    param = CameraAutoAdjuster()
    r = rospy.Rate(1000)
    # b = False
    while not rospy.is_shutdown():
        param.change_config()
        r.sleep()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass

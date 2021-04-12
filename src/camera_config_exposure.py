#!/usr/bin/env python

import rospy
import dynamic_reconfigure.client as dc
import dynamic_reconfigure.server as ds
import numpy as np
from std_msgs.msg import Float32


class CameraDefult:
    exposure = 0
    logexp = 1
    framerate = 12


class CameraParams:
    exposure = CameraDefult.exposure
    logexp = CameraDefult.logexp
    framerate =CameraDefult.framerate


class CameraAutoAdjuster:
    def __init__(self):
        self.sub = rospy.Subscriber("ref", Float32, self.ref_callback)
        self.ref = 100
        self.client = dc.Client("/camera/camera_nodelet", timeout=100,
                                                        config_callback=self.callback)
        self.target =100
        self.pL = 0.002

    def change_config(self):
        err = self.target - self.ref
        if err > 30 or err < -10:
            CameraParams.exposure += self.pL * err
            #CameraParams.logexp = max(min(CameraParams.logexp, 2.5), 1)
            #print(CameraParams.logexp)
            #CameraParams.logexp = 0
            #CameraParams.exposure = np.exp(CameraParams.logexp)
            print(CameraParams.logexp)
            
            config = {"auto_exposure": False,"exposure":CameraParams.exposure,
                      "auto_shutter": True,
                      "auto_gain": True,
                      "frame_rate": CameraParams.framerate,
                      "auto_white_balance": False, "white_balance_red": 690, "white_balance_blue":690} # # 
            #print("set config:", config)
            self.client.update_configuration(config)
        config = {"auto_white_balance": True}
        rospy.loginfo("err:{}".format(err))
        #else:
        #    config = {"auto_exposure": False,"exposure":CameraParams.exposure,       
        #              "auto_shutter": False,
        #              "auto_gain": False,
        #              "frame_rate": CameraParams.framerate} # 
            #print("set config:", config)
        #    self.client.update_configuration(config)

    def ref_callback(self, data):
        self.ref = data.data
        #print("ref value:", self.ref)

    def callback(self, config):
        rospy.loginfo("auto_exposure :{auto_exposure},exposure: {exposure}, shutter_speed:{shutter_speed}".format(**config))
        # CameraParams.shutter = config["shutter_speed"]
        # CameraParams.logshut = np.log(CameraParams.shutter)


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

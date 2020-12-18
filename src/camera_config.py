#!/usr/bin/env python

import rospy
import dynamic_reconfigure.client
import numpy as np
from std_msgs.msg import Float32


class CameraDefult:
    exposure = 0.7
    shutter = 0.01
    logshut = -2.
    gain = 0.
    framerate = 7


class CameraParams:
    exposure = CameraDefult.exposure
    shutter = CameraDefult.shutter
    logshut = CameraDefult.logshut
    gain = CameraDefult.gain
    framerate =CameraDefult.framerate


class CameraAutoAdjuster:
    def __init__(self):
        self.sub = rospy.Subscriber("ref", Float32, self.ref_callback)
        self.ref = 100
        self.client = dynamic_reconfigure.client.Client("/camera/camera_nodelet", timeout=30,
                                                        config_callback=self.callback)
        self.target = 200
        self.pE = -0.7
        self.pL = 0.01

    def change_config(self):
        err = self.target - self.ref
        CameraParams.logshut += self.pL * err
        CameraParams.logshut = max(min(CameraParams.logshut, -1), -4)
        CameraParams.shutter = np.exp(CameraParams.logshut)
        if CameraParams.logshut < -3:
            CameraParams.exposure = (CameraParams.logshut + 3) * self.pE
        elif CameraParams.logshut >= -1:
            CameraParams.exposure = (CameraParams.logshut + 2) * self.pE
        else:
            CameraParams.exposure = 0.7

        rospy.loginfo("err:{}".format(err))
        config = {"auto_exposure": False,"exposure":CameraParams.exposure,
                  "auto_shutter": False, "shutter_speed": CameraParams.shutter,
                  "auto_gain": False, "gain": CameraParams.gain,
                  "frame_rate": CameraParams.framerate}
        print("set config:", config)
        self.client.update_configuration(config)

    def ref_callback(self, data):
        self.ref = data.data
        print("ref value:", self.ref)

    def callback(self, config):
        rospy.loginfo("auto_exposure :{auto_exposure},exposure: {exposure}, "
                      "auto_shutter: {auto_shutter}, shutter_speed: {shutter_speed},"
                      " gain: {gain}".format(**config))
        # CameraParams.shutter = config["shutter_speed"]
        # CameraParams.logshut = np.log(CameraParams.shutter)


def main():
    rospy.init_node("dynamic_client")
    param = CameraAutoAdjuster()
    r = rospy.Rate(10)
    # b = False
    while not rospy.is_shutdown():
        param.change_config()
        r.sleep()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass

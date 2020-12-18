#!/usr/bin/env python

import rospy
import dynamic_reconfigure.client
import numpy as np
from std_msgs.msg import Float32

class Camera_Parameter:

    def __init__(self):
        self.sub = rospy.Subscriber("ref",Float32,self.ref_callback)
        self.ref = 0.0
        self.shutter = 0.03
        self.client = dynamic_reconfigure.client.Client("/camera/camera_nodelet", timeout=30, config_callback=self.callback)
        
    def change_config(self):
        ref = self.ref
        gain = 0
        framrate =10 
        target = 120
        b =False
        
        pE = 1
        r = rospy.Rate(0.1)
        pL =0.01
        exposure = 0.7
        #print("self.shutter",self.shutter * 1000)
        shutter = self.shutter * 1000
        err = target-ref
        shutter += pL * err
        #print("self.shutter",shutter)
        logshut = np.log(shutter)
        #print(logshut)

        
        

        logshut = max(min(logshut,2),-1)
        #print(logshut)
        if logshut < 0:
            exposure = logshut * pE
        if logshut >1:
            exposure = (logshut -1) * pE
        
        shutter_speed = np.exp(logshut)*0.001
        rospy.loginfo("err:{}".format(err))
        self.client.update_configuration({"auto_exposure":False,"exposure":exposure,"auto_shutter":False,"shutter_speed":shutter_speed,"auto_gain":False,"gain":0.0}) #   ,"shutter_speed":shutter
    
    
    def ref_callback(self,data):
        ref = data.data
        self.ref = ref


    def callback(self,config):
        #rospy.loginfo("Config test")
        #rospy.loginfo(config)
        
        rospy.loginfo("auto_exposure :{auto_exposure},exposure: {exposure}, auto_shutter: {auto_shutter}, shutter_speed: {shutter_speed}, gain: {gain}".format(**config))
        self.shutter= config["shutter_speed"]

def main():
    rospy.init_node("dynamic_client")
    param = Camera_Parameter()
    
    
    r = rospy.Rate(10)

    #b = False
    while not rospy.is_shutdown():
        param.change_config()
        r.sleep()



if __name__=="__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
    

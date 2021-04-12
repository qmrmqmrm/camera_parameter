#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example Python node to publish on a specific topic."""

# Import required Python code.
import rospy

# Give ourselves the ability to run a dynamic reconfigure server.
from dynamic_reconfigure.server import Server as DynamicReconfigureServer

# Import custom message data and dynamic reconfigure variables.
from node_example.msg import NodeExampleData
from pointgrey_camera_driver.cfg import PointGrey as ConfigType
from std_msgs.msg import Int32


class NodeExample(object):
    """Node example class."""

    def __init__(self):
        """Read in parameters."""
        # Get the private namespace parameters from the parameter server:
        # set from either command line or launch file.
        rate = rospy.get_param("~rate", 1.0)
        # Initialize enable variable so it can be used in dynamic reconfigure
        # callback upon startup.
        self.enable = True
        # Create a dynamic reconfigure server.
        self.server = DynamicReconfigureServer(ConfigType, self.reconfigure_cb)
        # Create a publisher for our custom message.
        self.pub = rospy.Publisher("example", Int32, queue_size=10)
        # Initialize message variables.
        #self.enable = rospy.get_param("~enable", True)
        #self.int_a = rospy.get_param("~a", 1)
        #self.int_b = rospy.get_param("~b", 2)
        #self.message = rospy.get_param("~message", "hello")

        if self.enable:
            self.start()
        else:
            self.stop()

        # Create a timer to go to a callback at a specified interval.
        rospy.Timer(rospy.Duration(1.0 / rate), self.timer_cb)

    def start(self):
        """Turn on publisher."""
        self.pub = rospy.Publisher("example", Int32, queue_size=10)

    def stop(self):
        """Turn off publisher."""
        self.pub.unregister()

    def timer_cb(self, _event):
        """Call at a specified interval to publish message."""
        if not self.enable:
            return

        # Set the message type to publish as our custom message.
        msg = Int32()
        # Assign message fields to values from the parameter server.
        #msg.message = rospy.get_param("~message", self.message)
        #msg.a = rospy.get_param("~a", self.int_a)
        msg.data = 32

        # Fill in custom message variables with values updated from dynamic
        # reconfigure server.
        #self.message = msg.message
        #self.int_a = msg.a
        #self.int_b = msg.b

        # Publish our custom message.
        self.pub.publish(msg)

    def reconfigure_cb(self, config, dummy):
        """Create a callback function for the dynamic reconfigure server."""
        # Fill in local variables with values received from dynamic reconfigure
        # clients (typically the GUI).
        self.exposure = config["exposure"]
        self.shutter_speed = config["shutter_speed"]
        self.frame_rate = config["frame_rate"]

        # Check to see if node should be started or stopped.
		print(self.exposure,self.shutter_speed,self.frame_rate )

        # Return the new variables.
        return config


# Main function.
if __name__ == "__main__":
    # Initialize the node and name it.
    rospy.init_node("pytalker")
    # Go to class functions that do all the heavy lifting.
    try:
        NodeExample()
    except rospy.ROSInterruptException:
        pass
    # Allow ROS to go to all callbacks.
    rospy.spin()

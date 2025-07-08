#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import os
from std_msgs.msg import String

class ActionGroupsPublisher:
    def __init__(self):
        # Node initialization
        rospy.init_node('action_groups_publisher')
        
        # Path to the data folder
        self.folder_path = "/home/ubuntu/software/ainex_controller/ActionGroups"
        
        # Create publisher for /action_groups_data topic
        self.pub = rospy.Publisher('/action_groups_data', String, queue_size=10)
        
        # Timer for periodic publishing (once per second)
        rospy.Timer(rospy.Duration(1), self.publish_data)
        
        rospy.loginfo("ActionGroups Publisher started and publishing data to /action_groups_data")

    def publish_data(self, event):
        try:
            # Get the list of files in the folder
            files = os.listdir(self.folder_path)
            
            # Form the data string
            data = "ActionGroups: " + ", ".join(files)
            
            # Publish the data
            self.pub.publish(data)
            
        except Exception as e:
            rospy.logerr("Error reading folder: %s", str(e))

if __name__ == '__main__':
    try:
        ActionGroupsPublisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import std_srvs.srv
import math
import time



class CamojiSender:

    def __init__(self):
        rospy.init_node('camoji', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/camoji1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/camoji/pose', Pose, self.when_data)
        self.pose = Pose()
        self.rate = rospy.Rate(10)


    def when_data(self, data):
        self.pose = data
        # self.pose.x = round(self.pose.x, 4)

    
    def send(self, start_x, array):
        serv1=rospy.ServiceProxy('camoji1/teleport_absolute',TeleportAbsolute)
        serv1(start_x, 6, -0.5*math.pi)
        vel_msg = Twist()
        vel_msg.linear.x = 1
        self.velocity_publisher.publish(vel_msg)
        time.sleep(1)
        
        
        

if __name__ == '__main__':
  try:
    camoji_sender = CamojiSender()
    camoji_sender.send()
  except rospy.ROSInterruptException:
    pass

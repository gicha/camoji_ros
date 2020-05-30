#!/usr/bin/env python
import rospy
from camoji.msg import Scan
import std_srvs.srv
import math
import time


class CamojiSender:

    def __init__(self):
        rospy.init_node('camoji', anonymous=True)
        self.scan_publisher = rospy.Publisher('/camoji/scanner', Scan, queue_size=1)
        for i in range(100):
            self.send()
            time.sleep(1)
        # self.pose_subscriber = rospy.Subscriber('/camoji/pose', Pose, self.when_data)

    
    def send(self):
        scan = Scan()
        scan.emotion = "neutral"
        scan.probability = 0.5
        scan.date = rospy.Time.now()
        scan.sex = 1
        scan.age = 10
        self.scan_publisher.publish(scan)


if __name__ == '__main__':
  try:
    camoji_sender = CamojiSender()
  except rospy.ROSInterruptException:
    pass

#!/usr/bin/env python
import rospy
from camoji.msg import Scan
import std_srvs.srv
from std_msgs.msg import String
from std_msgs.msg import Float32
import math
import time
from random import random


class CamojiSender:

    def __init__(self):
        rospy.init_node('camoji', anonymous=True)
        self.emotion_publisher = rospy.Publisher('emotion', String, queue_size=10)
        self.probability_publisher = rospy.Publisher('probability', Float32, queue_size=10)
        self.timer_publisher = rospy.Publisher('timer', String, queue_size=10)
        while True:
            self.send()
            time.sleep(1)

    def send(self):
        scan = Scan()
        random_emotion = random()
        if (random_emotion < 0.33):
            scan.emotion = "negative"
        elif (random_emotion < 0.66):
            scan.emotion = "neutral"
        else:
            scan.emotion = "positive"
        scan.probability = random()
        scan.date = rospy.Time.now()
        scan.sex = 1
        scan.age = 10
        self.emotion_publisher.publish(scan.emotion)
        self.probability_publisher.publish(scan.probability)
        self.timer_publisher.publish(str(rospy.get_time()))


if __name__ == '__main__':
  try:
    camoji_sender = CamojiSender()
  except rospy.ROSInterruptException:
    pass

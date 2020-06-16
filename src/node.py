#!/usr/bin/env python3
import rospy
from camoji.msg import Scan
import std_srvs.srv
from std_msgs.msg import String
from std_msgs.msg import Float32
import math
import time
from random import random
import cv2
import numpy as np
from keras.models import load_model
import sys
import datetime

class CamojiSender:

    def sendEmotion(self, emotion):
        self.emotion_publisher.publish(emotion)

    def sendTime(self):
        self.timer_publisher.publish(str(rospy.get_time()))

    # Если не встроенная вебка, то src = 1
    def web_cam(self):
        src = 0
        vid_rec = False
        face_detector = cv2.CascadeClassifier('/home/gicha/catkin_ws/src/camoji/src/model/haarcascade_frontalface_default.xml')
        model_em = load_model('/home/gicha/catkin_ws/src/camoji/src/model/emotion_recognition.h5')
        cap = cv2.VideoCapture(src)
        if not cap.isOpened():
            print("Can't start camera")
            sys.exit(0)

        # Опознования лица
        faceCascade = face_detector
        # Распознаваемые эмоции
        emotions = {0:'Angry',1:'Fear',2:'Happy',3:'Sad',4:'Surprised',5:'Neutral'}
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=7,
                minSize=(100, 100),
            )
            try:
                if len(faces) > 0:
                    for x, y, width, height in faces:
                        cropped_face = gray[y:y + height,x:x + width]
                        test_image = cv2.resize(cropped_face, (48, 48))
                        test_image = test_image.reshape([-1,48,48,1])
                        test_image = np.multiply(test_image, 1.0 / 255.0)
                        probab = model_em.predict(test_image)[0] * 100
                        label = np.argmax(probab)
                        predicted_emotion = emotions[label]
                        if predicted_emotion in ('Angry','Sad','Fear'):
                            predicted_reaction = 'Negative'
                        elif predicted_emotion in ('Happy','Surprised'):
                            predicted_reaction = 'Positive'
                        else:
                            predicted_reaction = 'Neutral'
                        self.sendEmotion(predicted_reaction)
                        self.sendTime()

    
            except Exception as error:
                print(error)
                pass

            cv2.imshow('frame', frame)

            # Жамкни букву q на клавиатуре, чтобы закрыть окно видео
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cv2.destroyAllWindows()
        f.close()

    def __init__(self):
        rospy.init_node('camoji', anonymous=True)
        self.emotion_publisher = rospy.Publisher('emotion', String, queue_size=10)
        self.probability_publisher = rospy.Publisher('probability', Float32, queue_size=10)
        self.timer_publisher = rospy.Publisher('timer', String, queue_size=10)
        self.web_cam()

    
    def sendRandom(self):
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
        self.timer_publisher.publish(str(rospy.get_time()))
        


if __name__ == '__main__':
  try:
    camoji_sender = CamojiSender()
  except rospy.ROSInterruptException:
    pass

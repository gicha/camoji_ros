# -*- coding: utf-8 -*-
"""
Created on Sun May 10 17:19:44 2020

@author: Wellery
"""


import cv2
import numpy as np
from keras.models import load_model
import sys

# Если не встроенная вебка, то src = 1
def web_cam(face_detector,model_em,src=0,vid_rec = False):

    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        print("Can't start camera")
        sys.exit(0)

    # Опознования лица
    faceCascade = face_detector
    
    # Для красоты оформления
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Распознаваемые эмоции
    emotions = {0:'Angry',1:'Fear',2:'Happy',3:'Sad',4:'Surprised',5:'Neutral'}
    
    while True:

        ret, frame = cap.read()
    
        # Проверка на ret = True
        if not ret:
            print("No image")
            break

        # Конвертация RGB в чб для детекции
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Распозновние лиц занимает примерно 0.07 сек
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=7,
            minSize=(100, 100),)

        try:
            f = open('./test.txt','w')
            # Отображение рамочек с эмоцией для всех лиц
            if len(faces) > 0:
                for x, y, width, height in faces:
                    
                    cropped_face = gray[y:y + height,x:x + width]
                    test_image = cv2.resize(cropped_face, (48, 48))
                    test_image = test_image.reshape([-1,48,48,1])

                    test_image = np.multiply(test_image, 1.0 / 255.0)

                    # Вероятности для всех типов эмоций
                    # Где-то 0.05 сек для находения вероятности на класс эмоции
                    probab = model_em.predict(test_image)[0] * 100

                    # Нахождение эмоции с наивысшей вероятностью
                    label = np.argmax(probab)
                    predicted_emotion = emotions[label]
                    
                    # Переделка на позитив/негатив
                    if predicted_emotion in ('Angry','Sad','Fear'):
                        predicted_reaction = 'Negative'
                    elif predicted_emotion in ('Happy','Surprised'):
                        predicted_reaction = 'Positive'
                    else:
                        predicted_reaction = 'Neutral'
                            
                   


        except Exception as error:
            print(error)
            pass

        cv2.imshow('frame', frame)

        # Жамкни букву q на клавиатуре, чтобы закрыть окно видео
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cv2.destroyAllWindows()
    f.close()

def main():

    face_detector = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')
    emotion_model = load_model('./model/emotion_recognition.h5')
    
    web_cam(face_detector,emotion_model)

if __name__ == '__main__':
    main()
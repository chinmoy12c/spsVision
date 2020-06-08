#!/bin/python3
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image
from time import sleep
import threading
import cv2
import numpy as np
import random
import pyttsx3

class Player(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.status = "HALT"
        self.timer = None
        self.cropped = None
        self.mySign = None
        self.choices = ['paper', 'scissor', 'stone']
        self.rules = {
            "paper" : "stone",
            "stone" : "scissor",
            "scissor" : "paper"
        }
        self.myScore = 0
        self.computerScore = 0
        self.replies = [
            ["I'll get you, next time.","You won.","I lost to, a human."],
            ["It's, a tie.", "I'll surpass you, soon"],
            ["Haha, I won", "Better luck, next time.", "I, am, unbeatable"]
        ]
        self.setModel()

    def setModel(self):
        print("Setting up model...")
        with open('modelFinal.json','r') as modelJson:
            self.model = model_from_json(modelJson.read())
        
        self.model.load_weights('modelWeights.h5')
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)

    def run(self):

        self.engine.say("Let's get started.")
        self.engine.runAndWait()
        while (True):
            if (self.status == "STOP"):
                break
            self.timer = "3"
            print("3...")
            sleep(1)
            if (self.status == "STOP"):
                break
            self.timer = "2"
            print("2...")
            sleep(1)
            if (self.status == "STOP"):
                break
            self.timer = "1"
            print("1...")
            sleep(1.5)

            self.mySign = random.choice(self.choices)
            cv2.imwrite('../res/tmp.png',self.cropped)
            loadedImg=image.load_img('../res/tmp.png', target_size=(150, 150))
            x=image.img_to_array(loadedImg)
            x=np.expand_dims(x, axis=0)
            x = x/255
            images = np.vstack([x])

            classes = self.model.predict(images)
            pred = self.choices[np.where(classes == np.amax(classes))[1][0]]
            print("You: {}, Computer: {}".format(pred,self.mySign))
            result = self.getResults(pred,self.mySign)
            print(result)
            self.engine.runAndWait()
            self.mySign = None

        print("Your score: {}, Computer's score: {}".format(self.myScore,self.computerScore))
    
    def getResults(self,pred, mySign):
        
        if (pred == mySign):
            self.engine.say(random.choice(self.replies[1]))
            return "TIE"
        elif (mySign == self.rules[pred]):
            self.myScore += 1
            self.engine.say(random.choice(self.replies[0]))
            return "WIN"
        else:
            self.computerScore += 1
            self.engine.say(random.choice(self.replies[2]))
            return "LOSE"

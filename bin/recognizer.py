#!/bin/python3
import cv2
import os
from Player import Player

class Recognizer():

    def __init__(self):
        super().__init__()
        self.startCapture()

    def startCapture(self):

        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)

        cv2.namedWindow("Player")

        start_point = (100,100)
        end_point = (400,400)
        color = (0,255,0)
        thickness = 2

        myPlayer = Player()
        background = cv2.imread("../res/background.png")
        paperPic = cv2.imread("../res/paper.png")
        scissorPic = cv2.imread("../res/scissor.png")
        stonePic = cv2.imread("../res/stone.png")

        while (True):
            if myPlayer.timer != None and myPlayer.mySign == None:
                newBack = background.copy()
                cv2.putText(newBack,myPlayer.timer, 
                            (100,300), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            10,
                            (0,255,0,255),
                            5)

                cv2.putText(newBack,
                            "Your score: {}, Computer's score: {}"
                            .format(myPlayer.myScore,myPlayer.computerScore), 
                            (10,30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.5,
                            (0,255,0,255),
                            2)

                cv2.imshow("Computer", newBack)

            elif myPlayer.mySign == "paper":
                cv2.imshow("Computer", paperPic)
            
            elif myPlayer.mySign == "stone":
                cv2.imshow("Computer", stonePic)
            
            elif myPlayer.mySign == "scissor":
                cv2.imshow("Computer", scissorPic)

            ret,frame = cam.read()
            if not ret:
                break

            myPlayer.cropped = frame[start_point[0]:end_point[0], start_point[1]:end_point[1]]
            frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
            cv2.putText(frame,"Place your hand inside this square", 
                            (100,80), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.5,
                            (0,255,0,255),
                            2)

            if (myPlayer.status == "HALT"):
                cv2.putText(frame,"Press space to start.", 
                            (10,30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.8,
                            (0,255,0,255),
                            2)

            cv2.imshow("Player", frame)

            k = cv2.waitKey(1)

            if (k%256 == 27):
                print("Escape hit, closing...")
                myPlayer.status = "STOP"
                os.remove("../res/tmp.png")
                break

            if (k%256 == 32):
                if myPlayer.status != "PLAYING":
                    myPlayer.status = "PLAYING"
                    myPlayer.start()

Recognizer()
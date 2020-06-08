#!/bin/python3
import cv2
from random import randint

letter_set = input("Enter class:")
dataset = input("Enter test/train:")
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)

cv2.namedWindow("Live")

start_point = (100,100)
end_point = (400,400)
color = (0,255,0)
thickness = 2

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
    cv2.imshow("Live", frame)
    frame = frame[start_point[0]:end_point[0], start_point[1]:end_point[1]]
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = '../datasets/{}/{}/{}_{}.png'.format(dataset,letter_set,letter_set,randint(0,1000000))
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))

cam.release()

cv2.destroyAllWindows()

import json
import os
import cv2
import time
import random


def generate_random():
    out = list()
    num_of_fingers = random.randint(0, 10)
    while len(out) < num_of_fingers:
        finger = random.randint(1, 10)
        if finger not in out:
            out.append(finger)
    return sorted(out)

def save(fingers, image):
    print(fingers, 'saved')

print(generate_random())

vcap = cv2.VideoCapture("rtsp://192.168.1.7:5303/h264_ulaw.sdp")
print('start')

while True:
    if not vcap.isOpened():
        time.sleep(5)

    (grabbed, image) = vcap.read()

    if not grabbed:
        break

    fingers = generate_random()

    cv2.putText(image, str(fingers), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow(str(fingers), image)
    cv2.waitKey(delay=100)

    save(fingers, image)

    cv2.destroyWindow(str(fingers))
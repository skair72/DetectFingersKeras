# Modify 'test1.jpg' and 'test2.jpg' to the images you want to predict on
import pickle
import time

from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
import cv2
import imutils

# dimensions of our images
img_width, img_height = 192, 108

# load the trained convolutional neural network and the multi-label
# binarizer
print("[INFO] loading network...")
model = load_model('BestNewGen_3.model')
mlb = pickle.loads(open('mlb.pickle', "rb").read())

vcap = cv2.VideoCapture("rtsp://192.168.43.18:5303/h264_ulaw.sdp")

print('start')

while True:
    if not vcap.isOpened():
        time.sleep(5)

    (grabbed, image) = vcap.read()

    if not grabbed:
        break

    output = imutils.resize(image, height=500)

    # pre-process the image for classification
    image = cv2.resize(image, (108, 192))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)


    # classify the input image then find the indexes of the two class
    # labels with the *largest* probability
    print("[INFO] classifying image...")
    proba = model.predict(image)[0]
    idxs = sorted(np.argsort(proba)) #[::-1][:2]
    print(idxs)
    # mlb.pickle

    # loop over the indexes of the high confidence class labels
    for (i, j) in enumerate(idxs):
        # build the label and draw the label on the image
        label = "{:.0f}".format(proba[j] * 100)
        print(label)

        cv2.circle(output, ((i * 80), 300 if i == 5 or i == 6 else 50), 15,
                   (0, 255, 0) if proba[j] > 0.35 else (0, 0, 255), -1)

        cv2.putText(output, label, ((i * 80 - 15), 300 if i == 5 or i == 6 else 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0) if proba[j] < 0.3 else (0, 0, 255), 2)

    # show the probabilities for each of the individual labels
    for (label, p) in zip(mlb.classes_, proba):
        # print("{}: {:.2f}%".format(label, p * 100))
        pass

    # show the output image
    cv2.imshow("Output", output)

    if cv2.waitKey(5) == 27:
        break

vcap.release()
cv2.destroyAllWindows()


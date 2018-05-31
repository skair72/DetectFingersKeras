# Modify 'test1.jpg' and 'test2.jpg' to the images you want to predict on
import time

from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import keras
import cv2 as cv
import imutils

# dimensions of our images
img_width, img_height = 192, 108

# load the model we saved
model = load_model('savedModel4.h5')

opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

#rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov
#rtsp://192.168.1.7:5303/h264_ulaw.sdp
#rtsp://admin:admin@192.168.70.33:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif
vcap = cv.VideoCapture("rtsp://192.168.1.7:5303/h264_ulaw.sdp")
#frame_max = vcap.get(cv.CAP_PROP_FRAME_COUNT)
#vcap.set(cv.CAP_PROP_FPS, 30)
print('start')
#start to find fingers on press key
#or
#write to buffer and get latest and delete bufer
while True:
    #frame_max = vcap.get(cv.CAP_PROP_FRAME_COUNT)
    #print(frame_max)
    #vcap.set(cv.CAP_PROP_POS_FRAMES, frame_max)
    if not vcap.isOpened():
        time.sleep(5)


    (grabbed, frame) = vcap.read()

    if not grabbed:
        break

    #vcap.set(cv.CAP_PROP_POS_FRAMES, frame_max)

    frame = imutils.resize(frame, height=108)

    x = image.img_to_array(frame)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = model.predict_classes(images, batch_size=11)

    cv.putText(frame, str(classes), (10, 30),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv.imshow('VIDEO', frame)

    if cv.waitKey(5) == 27:  # ESC key press
        break

# stop the timer and display FPS information

# do a bit of cleanup
vcap.release()
cv.destroyAllWindows()


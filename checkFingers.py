import json
import os
import cv2
import imutils

config = json.load(open('new_config.json'))
image_folder = 'newTrain'

images = list(os.walk(image_folder))[0][2]
good_images = g_pic = list(filter(lambda x: not x.startswith('.') and x.endswith('.jpg'), images))

for i in good_images:
    if 'flip' in i:
        continue
    cv_img = imutils.resize(cv2.imread(os.path.join(image_folder, i), cv2.COLOR_BGR2RGB), height=500)

    cv2.putText(cv_img, str(sorted(config[i])), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow(i, cv_img)
    cv2.waitKey(0)
    cv2.destroyWindow(i)
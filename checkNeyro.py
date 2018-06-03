import json
import os

import imutils
from shutil import copyfile
import cv2
from keras.preprocessing.image import img_to_array
import numpy as np
from keras.models import load_model
import pickle


photo_dir = 'newTrain'
out_dir = 'neyroErrors'
err_config_path = 'neyroErrors/config.json'
checked_path = 'neyroErrors/checked.json'
config_path = 'new_config.json'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
if not os.path.exists(err_config_path):
    json.dump(dict(), open(err_config_path, 'a'))
if not os.path.exists(checked_path):
    json.dump(list(), open(checked_path, 'a'))

err_config = json.load(open(err_config_path, 'r+'))
checked = json.load(open(checked_path, 'r+'))
config = json.load(open(config_path))


print("[INFO] loading network...")
img_width, img_height = 192, 108
model = load_model('newGen_17.model')
mlb = pickle.loads(open('mlb.pickle', "rb").read())

key_to_num = {
    48: False,
    49: True,
    53: None
}


def predict(image, drop):
    out = list()
    # pre-process the image for classification
    image = cv2.resize(image, (img_width, img_height))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # classify the input image then find the indexes of the two class
    # labels with the *largest* probability
    proba = model.predict(image)[0]
    idxs = sorted(np.argsort(proba))  # [::-1][:2]

    for (i, j) in enumerate(idxs, 1):
        # build the label and draw the label on the image

        if proba[j] > drop:
            out.append(int(mlb.classes_[j]))
    return out


def all_images(folder):
    files = list(os.walk(folder))[0][2]
    good_images = sorted(list(filter(lambda x: x.endswith('.jpg') or x.endswith('.png'), files)))
    a = len(good_images)
    for c, g in enumerate(good_images, 1):
        print(f'{c}/{a} ({g})')
        yield g


def cp_to_err_folder(image, fingers):
    print(f'neyro error: {image}')
    copyfile(os.path.join(photo_dir, image), os.path.join(out_dir, image))
    err_config.update({image: fingers})
    json.dump(err_config, open(err_config_path, 'w+'))


def change_config(image, fingers):
    print(f'my error: {image}')
    config.update({image: fingers})
    json.dump(config, open(config_path, 'w+'))

def input_fingers():
    fingers = input(f'input fingers: ').split(' ')
    return [int(i) for i in fingers]

def both_err(image):
    fingers = input_fingers()
    change_config(image, fingers)
    cp_to_err_folder(image, fingers)

def delete(image):
    os.remove(os.path.join(out_dir, image))
    del err_config[image]
    json.dump(config, open(config_path, 'w+'))

image_generator = all_images(photo_dir)

img_name = next(image_generator)
local_checked = list()
right_count = 0
while True:
    while img_name in err_config or img_name in checked:
        img_name = next(image_generator)

    img = imutils.resize(cv2.imread(os.path.join(photo_dir, img_name), 1), height=img_height*5, width=img_width*5)

    if img_name not in local_checked:
        local_checked.append(img_name)
        print('calculating...')
        config_fingers = sorted(config[img_name])
        neyro_fingers = sorted(predict(img, 0.6))

    if config_fingers == neyro_fingers:
        if img_name in err_config:
            right_count += 1
            print(f'{img_name} right, all {right_count}')
            delete(img_name)
        img_name = next(image_generator)
        continue

    for i in range(1, 11):
        x, y = ((i * 80), 300 if i == 5 or i == 6 else 50)

        cv2.rectangle(img, (x-16, y-16), (x+16, y+16), (0, 255, 0) if i in config_fingers else (0, 0, 255), -1)
        cv2.circle(img, (x, y), 15, (0, 255, 0) if i in neyro_fingers else (0, 0, 255), -1)

    cv2.imshow('choose fingers', img)

    k = cv2.waitKey(33)
    if k == 27:  # Esc key to stop
        break
    elif k == -1:  # normally -1 returned,so don't print it
        continue
    else:
        if k in key_to_num:
            json.dump(checked, open(checked_path, 'w+'))
            checked.extend(local_checked)
            if key_to_num[k] is None:
                both_err(img_name)
            elif key_to_num[k]:
                cp_to_err_folder(img_name, config_fingers)
            else:
                change_config(img_name, neyro_fingers)
            img_name = next(image_generator)
        else:
            print(k)

print(right_count)
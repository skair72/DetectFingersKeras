import os
import json

import imutils
from PIL import Image
import cv2
from keras.preprocessing.image import img_to_array
import numpy as np
from keras.models import load_model
import pickle

train_folder, new_train_folder = 'lab_record', 'newTrain'
json_name = '../new_config.json'

print("[INFO] loading network...")
model = load_model('newGen_15.model')
all_fingers = [i for i in range(1, 11)]
mlb = pickle.loads(open('mlb.pickle', "rb").read())


def input_fingers(l):
    fingers = input(f'input {l} fingers: ').split(' ')
    while len(fingers) != l and fingers[0] != 'y':
        print(f'wrong! {len(fingers)}')
        fingers = input(f'input {l} fingers: ').split(' ')
        pass
    if fingers[0] == 'y':
        return None
    else:
        return [int(i) for i in fingers]


def get_config(main_dir, j_name):
    path = os.path.join(main_dir, j_name)
    if os.path.isfile(path):
        config = json.load(open(path))
    else:
        config = dict()
        json.dump(config, open(path, 'a'))
    return config


def walk(main_dir, to_save):
    config = get_config(to_save, json_name)
    dirs = sorted([x for x in os.walk(main_dir)])
    for d in dirs[1:]:
        num = int(d[0].split('/')[1])
        g_pic = sorted(list(filter(lambda x: not x.startswith('.'), d[2])))
        a = len(g_pic)
        for c, g in enumerate(g_pic, 1):
            print(f'{g}: {c}/{a}')
            if g in config:
                print(f'{g} in already in config')
                continue

            else:
                img = Image.open(os.path.join(d[0], g))

                cv_img = imutils.resize(cv2.imread(os.path.join(d[0], g), 1), height=500)

                # pre-process the image for classification
                image = cv2.resize(cv_img, (192, 108))
                image = image.astype("float") / 255.0
                image = img_to_array(image)
                image = np.expand_dims(image, axis=0)

                proba = model.predict(image)[0]
                idxs = np.argsort(proba)  # [::-1][:2]
                # loop over the indexes of the high confidence class labels
                predicted = [int(mlb.classes_[i]) for i in sorted(idxs[::-1][:num])]
                print(str(predicted))
                print(' '.join([f'{proba[i]*100:.0f}' for i in sorted(idxs[::-1][:num])]))


                # mlb.pickle

                # loop over the indexes of the high confidence class labels
                for (i, j) in enumerate(sorted(idxs), 1):
                    # build the label and draw the label on the image
                    label = "{:.0f}".format(proba[j] * 100)

                    cv2.circle(cv_img, ((i * 80), 300 if i == 5 or i == 6 else 50), 15,
                               (0, 255, 0) if i in predicted else (0, 0, 255), -1)

                    cv2.putText(cv_img, label, ((i * 80 - 15), 300 if i == 5 or i == 6 else 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 255, 0) if i not in predicted else (0, 0, 255), 2)

                cv2.imshow('choose fingers', cv_img)
                cv2.waitKey(delay=100)

                if num == 0:
                    f = []
                elif num == 10:
                    f = all_fingers
                elif num > 5:
                    temp = input_fingers(10 - num)
                    if temp is None:
                        f = predicted
                    else:
                        f = list(set(all_fingers)-set(temp))
                else:
                    temp = input_fingers(num)
                    if temp is None:
                        f = predicted
                    else:
                        f = temp

                cv2.destroyWindow(g)
                img.save(os.path.join(to_save, g))
                img.close()

            print(f)
            config.update({g: f})
            json.dump(config, open(os.path.join(to_save, json_name), 'w+'))


def walk2(main_dir, to_save):
    for i in os.walk(to_save):
        g_pic = list(filter(lambda x: not x.startswith('.'), i[2]))

    not_in_folder = list()
    for i in get_config(to_save, json_name):
        if i not in g_pic:
            not_in_folder.append(i)

    print(not_in_folder)

    dirs = [x for x in os.walk(main_dir)]
    for d in dirs[1:]:
        g_pic = list(filter(lambda x: not x.startswith('.'), d[2]))
        for g in g_pic:
            if g in not_in_folder:
                print(g)
                img = Image.open(os.path.join(d[0], g))
                img.save(os.path.join(to_save, g))
                img.close()


walk(train_folder, new_train_folder)
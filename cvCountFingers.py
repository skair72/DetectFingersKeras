import cv2
import os
import imutils
from PIL import Image


key_to_num = {
    48: 0,
    49: 1,
    50: 2,
    51: 3,
    52: 4,
    53: 5,
    54: 6,
    55: 7,
    56: 8,
    57: 9,
    100: -1,
    113: 10
}

old_folder = 'storage/snap2'
new_folder = 'lab_record'

if not os.path.exists(new_folder):
    os.makedirs(new_folder)


def get_parsed_photos(path):
    all_images = list()
    dirs = [x for x in os.walk(path)]
    for d in dirs[1:]:
        # num = int(d[0].split('/')[1])
        g_pic = sorted(list(filter(lambda x: x.endswith('.jpg'), d[2])))
        for g in g_pic:
            all_images.append(g)
    return all_images


def all_images(folder):
    files = list(os.walk(folder))[0][2]
    good_images = sorted(list(filter(lambda x: x.endswith('.jpg'), files)))
    a = len(good_images)
    for c, g in enumerate(good_images, 1):
        print(f'{c}/{a} ({g})')
        yield g


def save_image(old, new, name):
    print(new)
    if not os.path.exists(new):
        os.makedirs(f'{new}')
    path = os.path.join(old, name)
    image = Image.open(path)
    image.save(os.path.join(new, name))
    image.close()


def delete_image(old, name):
    path = os.path.join(old, name)
    os.remove(path)


image_generator = all_images(old_folder)
img_name = next(image_generator)
mem = get_parsed_photos(new_folder)

while True:
    while img_name in mem:
        img_name = next(image_generator)
    img = imutils.resize(cv2.imread(os.path.join(old_folder, img_name), 1), height=400)

    cv2.imshow('count fingers', img)
    k = cv2.waitKey(33)

    if k == 27:    # Esc key to stop
        break
    elif k == -1:  # normally -1 returned,so don't print it
        continue
    else:
        if k in key_to_num:
            mem.append(img_name)
            if key_to_num[k] >= 0:
                save_image(old_folder, os.path.join(new_folder, str(key_to_num[k])), img_name)
            else:
                delete_image(old_folder, img_name)
            img_name = next(image_generator)
        else:
            print(k)

cv2.destroyAllWindows()

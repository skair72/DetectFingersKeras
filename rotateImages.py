import json
import os
from PIL import Image

photo_dir = 'storage/snap'
images = list(os.walk(photo_dir))[0][2]


def flip(name):
    path = os.path.join(photo_dir, name)
    image = Image.open(path).transpose(Image.ROTATE_180)
    image.save(os.path.join(photo_dir, name))
    #image.show()
    image.close()


def by_group(starts):
    good_images = list(filter(lambda x: x.startswith(starts) and x.endswith('.jpg'), images))
    a = len(good_images)
    for c, img in enumerate(good_images, 1):
        flip(img)
        print(f'{starts}: {c}/{a}')


by_group('fingers13_')
by_group('fingers14_')
by_group('fingers15_')
by_group('fingers16_')
by_group('fingers17_')
by_group('fingers18_')
by_group('fingers19_')
import json
import os
from PIL import Image

config = json.load(open('unicTrain/config.json'))
photo_dir = 'unicTrain'

images = list(os.walk(photo_dir))[0][2]
good_images = g_pic = list(filter(lambda x: not x.startswith('flip') and (x.endswith('.jpg') or x.endswith('.png')), images))

def flip(name):
    path = os.path.join(photo_dir, name)
    image = Image.open(path).transpose(Image.FLIP_LEFT_RIGHT)
    image.save(os.path.join(photo_dir, 'flip_' + name))
    image.close()
    config.update({'flip_' + name: [11 - i for i in config[name]]})


a = len(good_images)
for c, img in enumerate(good_images, 1):
    if os.path.exists(os.path.join(photo_dir, 'flip_' + img)):
        continue
    flip(img)
    print(f'{c}/{a}')

json.dump(config, open('unicTrain/config.json', 'w+'))

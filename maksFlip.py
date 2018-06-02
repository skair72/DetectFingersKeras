import os
from PIL import Image

foler_to_flip = 'maxTrain'
folders = sorted([x for x in os.walk(foler_to_flip)])

#good_images = sorted(list(filter(lambda x: x.endswith('.jpg'), images)))

for d in folders[1:]:
    foler = d[0]
    images = d[2]
    for i in images:
        full_image_path = os.path.join(foler, i)
        image = Image.open(full_image_path).transpose(Image.FLIP_TOP_BOTTOM)
        image.save(full_image_path)
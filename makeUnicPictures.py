import os
import json
from shutil import copyfile
import random

foler_to_parse = 'newTrain'
foler_to_save = 'unicTrain'

if not os.path.exists(foler_to_save):
    os.makedirs(foler_to_save)

json_to_parse = 'new_config.json'
json_to_save = os.path.join(foler_to_save, 'config.json')

old_config = json.load(open(json_to_parse, 'r+'))

images = list(os.walk(foler_to_parse))[0][2]
good_images = sorted(list(filter(lambda x: not x.startswith('flip') and (x.endswith('.jpg') or x.endswith('.png')), images)))
prefix = good_images[0][:10]
all_combinations = dict()
temp_combinations = dict()
l = len(good_images)

for c, i in enumerate(good_images, 1):
    print(f'{c}/{l}')
    current_prefix = i[:10]
    if current_prefix == prefix:
        current_combination = old_config[i]
        if current_combination in temp_combinations.values():
            continue
        else:
            temp_combinations.update({i: current_combination})
            copyfile(os.path.join(foler_to_parse, i), os.path.join(foler_to_save, i))
    else:
        all_combinations.update(temp_combinations)
        temp_combinations.clear()
        prefix = current_prefix

all_combinations.update(temp_combinations)
json.dump(all_combinations, open(json_to_save, 'w+'))

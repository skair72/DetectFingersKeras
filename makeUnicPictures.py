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
good_images = sorted(list(filter(lambda x: (x.endswith('.jpg') or x.endswith('.png')), images)))
prefix = good_images[0][:10]
all_combinations = dict()
prefix_good_images = dict()

temp_combinations = dict()
l = len(good_images)


def get_unic_from_dict(d):
    unic_combinations = dict()
    for j in d:
        current_combination = old_config[j]
        if current_combination in unic_combinations.values():
            continue
        else:
            unic_combinations.update({j: current_combination})
            copyfile(os.path.join(foler_to_parse, j), os.path.join(foler_to_save, j))
    print(f'in {len(d)}; out {len(unic_combinations)}')
    return unic_combinations


for c, i in enumerate(good_images, 1):
    current_prefix = i[:10]
    if current_prefix == prefix:
        temp_combinations.update({i: old_config[i]})
    else:
        all_combinations.update(get_unic_from_dict(temp_combinations))
        temp_combinations.clear()
        prefix = current_prefix

all_combinations.update(get_unic_from_dict(temp_combinations))
json.dump(all_combinations, open(json_to_save, 'w+'))

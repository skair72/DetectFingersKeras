import json

old = json.load(open('config.json'))
new = dict()

for key, value in old.items():
    new_arr = list()

    for c, v in enumerate(value, 1):
        if v:
            new_arr.append(c)

    new.update({key: new_arr})

json.dump(new, open('new_config.json', 'a'))

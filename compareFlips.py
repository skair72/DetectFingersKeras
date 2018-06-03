import json

config_path = 'new_config.json'
config = json.load(open(config_path))
all_fingers = set([i for i in range(1, 11)])

for i in config:
    if not i.startswith('flip'):
        img = sorted(config[i])
        flip_img = sorted(11 - i for i in config[f'flip_{i}'])
        if img != flip_img:
            print(f'{i}: real {img}, flip {flip_img}')
            good = int(input(f'good real(1)/flip(2)'))
            while good != 1 and good != 2:
                good = int(input('good real(1)/flip(2) '))

            if good == 2:
                config[i] = flip_img
            else:
                config[f'flip_{i}'] = sorted(11 - i for i in img)
            json.dump(config, open(config_path, 'w+'))
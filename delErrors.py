import os
import json

main_dir = 'dina_nikita'
j = 'new_config.json'

config = json.load(open(j, 'r+'))

dirs = sorted([x for x in os.walk(main_dir)])
for d in dirs[1:]:
    num = int(d[0].split('/')[1])
    g_pic = sorted(list(filter(lambda x: not x.startswith('.'), d[2])))
    a = len(g_pic)
    for c, g in enumerate(g_pic, 1):
        if len(config[g]) != num:
            need = list()
            for i in range(1, 11):
                if i not in config[g]:
                    need.append(i)
            print(f'{g}: num: {num}, real: {len(config[g])}, {config[g]}')
            config[g] = need

print(config)
json.dump(config, open(j, 'w+'))

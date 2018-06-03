import json

checking_config = json.load(open('unicTrain/config.json', 'r+'))
checked_config = json.load(open('new_config.json', 'r+'))

for i in checking_config:
    checking = checking_config[i]
    checked = checked_config[i]
    if checking != checked:
        print(f'{i}: {checking} -> {checked}')
        checking_config[i] = checked

json.dump(checking_config, open('unicTrain/config.json', 'w+'))

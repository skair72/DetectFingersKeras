import os
from random import shuffle
from math import floor
from shutil import copyfile

def delBad(main_dir):
    dirs = [x for x in os.walk(main_dir)]
    for d in dirs[1:]:
        g_pic = list(filter(lambda x: not x.startswith('.'), d[2]))
        for g in g_pic:
            if g.startswith('flip'):
                os.remove(d[0] + '/' + g)

def to_train_and_test_dir(main_dir):
    dirs = [x for x in os.walk(main_dir)]
    count = 0
    for d in dirs[1:]:
        g_pic = list(filter(lambda x: not x.startswith('.'), d[2]))
        shuffle(g_pic)
        train = floor(len(g_pic) * 0.8)
        for i in range(len(g_pic)):
            if i < train:
                folder_name = d[0].replace(main_dir, 'train')
            else:
                folder_name = d[0].replace(main_dir, 'test')
            if not os.path.isdir(folder_name):
                os.makedirs(folder_name)
            copyfile(d[0] + '/' + g_pic[i], folder_name + '/' + g_pic[i])
            print(folder_name + '/' + g_pic[i])
            count += 1
    print(count)

#to_train_and_test_dir('blackPhoto')

to_train_and_test_dir('tshirtPhoto')
import os

startDir = 'all'


def good_pictures(main_dir):
    dirs = [x for x in os.walk(main_dir)]
    for d in dirs[1:]:
        g_pic = list(filter(lambda x: not x.startswith('.'), d[2]))
        for g in g_pic:
            yield d[0] + '/', g


if __name__ == "__main__":
    dirs = [x for x in os.walk(startDir)]
    for d in dirs[1:]:
        g_pic = list(filter(lambda x: not x.startswith('.'), d[2]))
        print(d[0], len(g_pic))

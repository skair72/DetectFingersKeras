from PIL import Image
import dirs


def rotate(p):
    for path, name in dirs.good_pictures(p):
        img = Image.open(path + name)
        img2 = img.rotate(-90, expand=True)
        img.close()
        img2.save(path + name)
        img2.close()
        print(name)


def flip(p):
    c = 0
    for path, name in dirs.good_pictures(p):
        c += 1
        img = Image.open(path + name).transpose(Image.FLIP_LEFT_RIGHT)
        img.save(path + 'flip_' + name)
        c += 1
        print(name, c)


rotate('blackPhoto')

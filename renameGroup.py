import os
main_dir = 'storage/snap2'
images = list(os.walk(main_dir))[0][2]
good_images = list(filter(lambda x: (x.endswith('.jpg')), images))

for fm in good_images:
    if fm.startswith('fingers19'):
        sname = fm.split('_')
        sname[0] = 'fingers20'
        os.rename(os.path.join(main_dir, fm), os.path.join(main_dir, '_'.join(sname)))
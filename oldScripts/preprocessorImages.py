from keras.preprocessing.image import array_to_img, img_to_array, load_img, ImageDataGenerator
import os

train_datagen = ImageDataGenerator(
        rotation_range=60,
        width_shift_range=0.1,
        height_shift_range=0.1,
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.1,
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode='nearest')

newGen = ImageDataGenerator(rotation_range=40, width_shift_range=-0.1, height_shift_range=-0.1, shear_range=0.2,
                            zoom_range=-0.2, fill_mode="nearest", horizontal_flip=True)


img = load_img('../newTrain/fingers12_00232.jpg')  # this is a PIL image
x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

# the .flow() command below generates batches of randomly transformed images
# and saves the results to the `preview/` directory
i = 0

folder_name = 'preview'
if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

for batch in newGen.flow(x, batch_size=1,  save_to_dir=folder_name, save_prefix='', save_format='jpg'):
        i += 1
        if i > 10:
                break
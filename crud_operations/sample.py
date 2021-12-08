from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import matplotlib.pyplot as plt

img_path = '/home/new/CURD-Django/crud_django/images/090114.jpg.jpg'

img = load_img(img_path, target_size = (224, 224, 3))
img = img_to_array(img)
print(img.shape)
print(len(img))
plt.imshow(img)
import cv2
import os
import image_reader as reader
import numpy as np
import augment

def are_images_equal(img1, img2):
    if img1.shape != img2.shape:
        return False
    return np.all(img1 == img2)

def read_file(name):
    with open(os.path.join(name), 'r') as file:
        return file.read()

test_cases = ['biden.jpg', 'test.jpg', 'forest.png']
messages = [read_file('declaration.txt'), '', 'abcdefghijklmnopqrstuvwxyz', '12345678910~!@#$%^&*()_+<>?:"|']
images_dir = 'test_images'

for case in test_cases:
    print('Test case: ', case)
    for msg in messages:
        filepath = os.path.join(images_dir)
        print(filepath)
        img = cv2.imread(filepath)


"""
with open('declaration.txt', 'r') as file:
    m3 = file.read().replace('\n', '')


biden = cv2.imread('C:\\Users\\drago\\OneDrive\\Desktop\\Steg\\biden.jpg')
print(biden.dtype)
biden = augment.add_gaussian_noise(biden, 5, 5)
print(biden.dtype)
reader.embed(biden, m3)
cv2.imwrite('biden-encoded.png', biden)
biden_encoded = cv2.imread('C:\\Users\\drago\\OneDrive\\Desktop\\Steg\\biden-encoded.png')
print(reader.decode(biden))

"""
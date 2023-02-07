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

#make sure 
def test_image(img, msg):
    encoded = reader.embed(img, msg)
    decoded = reader.decode(encoded)
    print('Passed: messages are equal') if decoded == msg else print('Failed: messages are not equal')

test_cases = ['biden.jpg', 'test.jpg', 'forest.png']
messages = [read_file('declaration.txt'), '', 'abcdefghijklmnopqrstuvwxyz', '12345678910~!@#$%^&*()_+<>?:"|']
images_dir = 'test_images'

for case in test_cases:
    print()
    print('Test case: ', case)
    for msg in messages:
        filepath = os.path.join(os.getcwd(), images_dir, case)
        img = cv2.imread(filepath)
        if img is not None:
            test_image(img, msg)
        else:
            print(f'Error: the image {case} could not be read')
            print()
            break

import numpy as np

#add a gaussian noise to an image
def add_gaussian_noise(img, mean=0, sigma=1):
    noise = np.random.normal(mean, sigma, img.shape)
    noisy_img = np.clip(img + noise, 0, 255).astype(np.uint8)
    return noisy_img


def add_salt_pepper_noise(img, salt_ratio=0.05, pepper_ratio=0.05):
    noise = np.zeros(img.shape, dtype=np.uint8)
    num_salt = int(np.ceil(img.size * salt_ratio))
    num_salt = min(num_salt, noise.size)
    coords = [np.random.randint(0, i - 1, num_salt) for i in img.shape]
    noise[coords] = 255
    num_pepper = int(np.ceil(img.size * pepper_ratio))
    num_pepper = min(num_pepper, noise.size)
    coords = [np.random.randint(0, i - 1, num_pepper) for i in img.shape]
    noise[coords] = 0
    noisy_img = np.clip(img + noise, 0, 255).astype(np.uint8)
    return noisy_img




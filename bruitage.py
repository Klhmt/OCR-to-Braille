from skimage.util import random_noise
import cv2
import matplotlib.pyplot as plt


# Charger l'image
image = cv2.imread('OCR-to-Braille/Alphabet_hugo/Alphabet_arial_taille11_lettres_minuscules/a.png')
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# (thresh, image_binary) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

noise = ['gaussian', 'localvar', 'poisson', 'salt', 'pepper', 's&p', 'speckle']

plt.figure()
for i in range (len(noise)) : 
    new_image = random_noise(image, noise[i])
    plt.subplot(2, 4, i+1)
    plt.imshow(new_image)
    plt.title(f'noise : {noise[i]}')
plt.show()

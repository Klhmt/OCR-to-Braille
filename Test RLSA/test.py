# convert the image to binary
import cv2
import matplotlib.pyplot as plt

image = cv2.imread('D:\Test RLSA\im.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
(thresh, image_binary) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# function call
import rlsa
image_rlsa_horizontal = rlsa.rlsa(image_binary, True, False, 10)
#print(type(image_rlsa_horizontal))

plt.figure()
plt.imshow(image_rlsa_horizontal, cmap=plt.cm.gray)
plt.show()

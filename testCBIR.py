import cv2
import matplotlib.pyplot as plt
from utils.color_conversion import rgb2hmmd

img = cv2.imread('ukbench00000.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV usa BGR
hmmd = rgb2hmmd(img_rgb, mode='HDS')
hmmdplot = plt.imshow(hmmd)
plt.show()
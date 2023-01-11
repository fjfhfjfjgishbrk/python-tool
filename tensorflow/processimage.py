import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import cv2


def calc(image):
    lowerLimit = 5

    oldHeight, oldWidth = image[:, :, 0].shape;
    ndviImage = np.zeros((oldHeight, oldWidth, 3), np.uint8)  # make a blank RGB image
    ndvi = np.zeros((oldHeight, oldWidth), np.int)  # make a blank b/w image for storing NDVI value
    red = np.zeros((oldHeight, oldWidth), np.int)  # make a blank array for red
    blue = np.zeros((oldHeight, oldWidth), np.int)

    red = (image[:, :, 2]).astype('float')
    green = (image[:, :, 1]).astype('float')
    blue = (image[:, :, 0]).astype('float')

    blue[blue < lowerLimit] = lowerLimit
    ndvi = ((((2*red-blue)/blue)/2+0.5)*255).astype('uint8')


    colorMap = cm.get_cmap("RdYlGn", 256)
    oceanMap = cm.get_cmap("bwr", 256)
    ndviImage = np.asarray(colorMap(ndvi)[:,:,:-1] * 255)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if red[i, j] < 60 and blue[i, j] > (1.9 * red[i, j]) and ndvi[i, j] < 120 and blue[i, j] > 70:
                ndviImage[i, j] = np.asarray(oceanMap(ndvi[i, j])[:-1]) * 255

    ndviImage = np.flip(ndviImage, axis=2)

    return ndviImage

img = cv2.imread('lower res test.jpg')
outImg = calc(img)
cv2.imwrite("aaadwef.jpg", outImg)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import cv2
import numpy as np
from datetime import datetime
import time
import os
import random
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow import keras
import math
import datetime
import processimage



img = cv2.imread('lower res test.jpg')

model = keras.models.load_model("models/model-pixel")


SIZE = 30
CHANGE_SIZE = 30
WHITE = np.full(3, 255)

height = SIZE
width = SIZE
shrink = (SIZE - CHANGE_SIZE) // 2
imgwidth = img.shape[0]
imgheight = img.shape[1]
totalCuts = (math.ceil(imgwidth / CHANGE_SIZE)) * (math.ceil(imgheight / CHANGE_SIZE))
count = 0
box = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
img = img[:width * (imgwidth // width), :height * (imgheight // height), :]
imgwidth = img.shape[0]
imgheight = img.shape[1]
predictArray = np.zeros((math.ceil(imgwidth / CHANGE_SIZE), math.ceil(imgheight / CHANGE_SIZE)))

a = 0
b = 0
aShape = predictArray.shape[0]
bShape = predictArray.shape[1]
timeStart = int(time.time() * 1000)
outImg = np.copy(img)
for i in range(0, imgheight, CHANGE_SIZE):
    for j in range(0, imgwidth, CHANGE_SIZE):
        count += 1
        cut = img[j: j + width, i: i + height, :]
        change = img[j + shrink: j + CHANGE_SIZE + shrink, i + shrink: i + CHANGE_SIZE + shrink, :]
        if cut.shape != (height, width, 3):
            continue
        out = model.predict(np.array([cut]))[0]
        ndviCut = processimage.calc(change)
        for w in range(CHANGE_SIZE):
            for h in range(CHANGE_SIZE):
                if out[w + h * CHANGE_SIZE] < 0.5:
                    for colors in range(3):
                        outImg[j + shrink + w, i + shrink + h, colors] = ndviCut[w, h, colors]
                else:
                    outImg[j + shrink + w, i + shrink + h, :] = WHITE
        now = int(time.time() * 1000)
        totalBox = 30
        percent = count / totalCuts
        boxDisplay = math.ceil(totalBox * percent)
        boxB = math.floor((totalBox * percent - boxDisplay) * 8)
        text = "█" * (boxDisplay - 1) + box[boxB] + " " * (totalBox - boxDisplay)
        est = ((now - timeStart) / (count / totalCuts) - (now - timeStart)) / 1000
        sec = datetime.datetime.now().second % 5
        loadingText = "-" * sec + " " * (4 - sec)
        print("\r", "Processing image |", text,
              "| [%d / %d] %.2f%% done  Est: %.2f sec left  %s Processing section (%d, %d)" % (count, totalCuts, percent * 100, est, loadingText, a, b), end="", sep="")
        a += 1
    b += 1
    a = 0

print("\r", "Finished processing image!", sep="")

cv2.imwrite("output/outPixel.jpg", outImg)

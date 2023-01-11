import cv2
import numpy as np
from datetime import datetime
import os
import random
from os import listdir
from os.path import isfile, join

data = [f for f in listdir("picture data/pixel/input") if isfile(join("picture data/pixel/input", f))]
predict = [f for f in listdir("picture data/pixel/output") if isfile(join("picture data/pixel/output", f))]

filelist = [f for f in os.listdir("pixeldata/input")]
for f in filelist:
    os.remove(os.path.join("pixeldata/input", f))

filelist = [f for f in os.listdir("pixeldata/output")]
for f in filelist:
    os.remove(os.path.join("pixeldata/output", f))

print("File cleared!")

SIZE = 30
LIMIT = 3000

WHITE = np.full(3, 255)
BLACK = np.zeros(3)
shrink = (SIZE - 6) // 2

def readImg(fileTrain, fileRes, t):
    imgTrain = cv2.imread("picture data/pixel/input/" + fileTrain)
    imgwidth = imgTrain.shape[0]
    imgheight = imgTrain.shape[1]
    height = SIZE
    width = SIZE
    imgTrain = imgTrain[:width * (imgwidth // width), :height * (imgheight // height), :]
    imgTrain = imgTrain[shrink:-shrink, shrink:-shrink, :]
    imgResult = cv2.imread("picture data/pixel/output/" + fileRes)
    imgwidth = imgTrain.shape[0]
    imgheight = imgTrain.shape[1]
    count = 0
    for i in range(0, imgheight):
        for j in range(0, imgwidth):
            a = imgTrain[j: j+width, i: i+height, :].copy()
            b = imgResult[j: j + width, i: i + height, :].copy()
            if a.shape != (height, width, 3):
                continue
            if random.random() < 0.002:
                count += 1
                if random.random() < 0.5:
                    c = random.randint(-1, 1)
                    a = cv2.flip(a, c)
                    b = cv2.flip(b, c)
                date = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
                cv2.imwrite("pixeldata/input/image_%s_%d.jpg" % (date, t + count), a)
                for k in range(0, height):
                    for l in range(0, width):
                        if not np.array_equal(b[l, k, :], WHITE):
                            b[l, k, :] = BLACK.copy()
                cv2.imwrite("pixeldata/output/image_%s_%d.jpg" % (date, t + count), b)
                print("\r", "Loading %s with %d pictures" % (fileTrain, count), end="", sep="")
            if count > LIMIT:
                break
        if count > LIMIT:
            break
    print("\r", "Done loading %s with %d pictures" % (fileTrain, count), sep="")
    return count

total = 0
for i in range(len(data)):
    fi = data[i]
    fo = predict[i]
    if fi.endswith("jpg") or fi.endswith("jpeg"):
        total += readImg(fi, fo, total)
print("============================")
print("Done loading buildings with %d pictures!" % total)
print("============================")

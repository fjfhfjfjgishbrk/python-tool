import cv2
import numpy as np
from datetime import datetime
import os
import random
from os import listdir
from os.path import isfile, join

# Save image in set directory
# Read RGB image
buildings = [f for f in listdir("picture data/landsat/buildings") if isfile(join("picture data/landsat/buildings", f))]
nonBuildings = [f for f in listdir("picture data/landsat/no") if isfile(join("picture data/landsat/no", f))]

filelist = [f for f in os.listdir("landSatBigData/build")]
for f in filelist:
    os.remove(os.path.join("landSatBigData/build", f))

filelist = [f for f in os.listdir("landSatBigData/no")]
for f in filelist:
    os.remove(os.path.join("landSatBigData/no", f))

print("File cleared!")

#img = cv2.imread('picture data/landsat/aaa39.jpg'

SIZE = 30
LIMIT = 1000

def readImg(filename, buildings, t):
    if buildings:
        img = cv2.imread("picture data/landsat/buildings/" + filename)
    else:
        img = cv2.imread("picture data/landsat/no/" + filename)
    height = SIZE
    width = SIZE
    imgwidth = img.shape[0]
    imgheight = img.shape[1]
    count = 0
    for i in range(0, imgheight):
        for j in range(0, imgwidth):
            a = img[j: j+width, i: i+height, :]
            if a.shape != (height, width, 3):
                continue
            try:
                if random.random() < 0.0013:
                    count += 1
                    if random.random() < 0.5:
                        a = cv2.flip(a, random.randint(-1, 1))
                    date = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
                    if buildings:
                        cv2.imwrite("landSatBigData/build/image_%s_%d.jpg" % (date, t + count), a)
                    else:
                        cv2.imwrite("landSatBigData/no/image_%s_%d.jpg" % (date, t + count), a)
                    print("\r", "Loading %s with %d pictures" % (filename, count), end="", sep="")
            except:
                pass
            if count > LIMIT:
                break
        if count > LIMIT:
            break
    print("\r", "Done loading %s with %d pictures" % (filename, count), sep="")
    return count


total = 0
for f in buildings:
    if f.endswith("jpg"):
        total += readImg(f, True, total)
print("============================")
print("Done loading buildings with %d pictures!" % total)
print("============================")

total = 0
for f in nonBuildings:
    if f.endswith("jpg"):
        total += readImg(f, False, total)
print("============================")
print("Done loading non-buildings with %d pictures!" % total)
print("============================")
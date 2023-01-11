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


#NDVI Calculation
#Input: an RGB image frame from infrablue source (blue is blue, red is pretty much infrared)
#Output: an RGB frame with equivalent NDVI of the input frame
def NDVICalc(original):
    "This function performs the NDVI calculation and returns an RGB frame)"
    lowerLimit = 5  #this is to avoid divide by zero and other weird stuff when color is near black

    #First, make containers
    oldHeight, oldWidth = original[:,:,0].shape;
    ndviImage = np.zeros((oldHeight,oldWidth,3),np.uint8) #make a blank RGB image
    ndvi = np.zeros((oldHeight,oldWidth),np.int) #make a blank b/w image for storing NDVI value
    red = np.zeros((oldHeight,oldWidth),np.int) #make a blank array for red
    blue = np.zeros((oldHeight,oldWidth),np.int) #make a blank array for blue

    #Now get the specific channels. Remember: (B , G , R)
    red = (original[:,:,2]).astype('float')
    blue = (original[:,:,0]).astype('float')

    #Perform NDVI calculation
    summ = red+blue
    summ[summ<lowerLimit] = lowerLimit #do some saturation to prevent low intensity noise

    ndvi = (((red-blue)/(summ)+1)*127).astype('uint8')  #the index

    redSat = (ndvi-128)*2  #red channel
    bluSat = ((255-ndvi)-128)*2 #blue channel
    redSat[ndvi<128] = 0; #if the NDVI is negative, no red info
    bluSat[ndvi>=128] = 0; #if the NDVI is positive, no blue info


    #And finally output the image. Remember: (B , G , R)
    #Red Channel
    ndviImage[:,:,2] = redSat

    #Blue Channel
    ndviImage[:,:,0] = bluSat

    #Green Channel
    ndviImage[:,:,1] = 255-(bluSat+redSat)

    return ndviImage;



img = cv2.imread('many buildings.jpg')

model = keras.models.load_model("models/model-hugeLandsat")


SIZE = 30
CHANGE_SIZE = 6

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
for i in range(0, imgheight, CHANGE_SIZE):
    for j in range(0, imgwidth, CHANGE_SIZE):
        count += 1
        cut = img[j: j + width, i: i + height, :]
        change = img[j + shrink: j + CHANGE_SIZE + shrink, i + shrink: i + CHANGE_SIZE + shrink, :]
        if cut.shape != (height, width, 3):
            continue
        out = model.predict(np.array([cut]))
        if out[0, 0] > out[0, 1]:
            for k in range(5):
                for l in range(5):
                    indexA = a - 2 + k
                    indexB = b - 2 + l
                    if 0 < indexA < aShape and 0 < indexB < bShape:
                        predictArray[indexA, indexB] += 1

        now = int(time.time() * 1000)
        totalBox = 30
        percent = count / totalCuts
        boxDisplay = math.ceil(totalBox * percent)
        boxB = math.floor((totalBox * percent - boxDisplay) * 8)
        text = "█" * (boxDisplay - 1) + box[boxB] + " " * (totalBox - boxDisplay)
        est = ((now - timeStart) / (count / totalCuts) - (now - timeStart)) / 1000
        sec = datetime.datetime.now().second % 5
        loadingText = "-" * sec + " " * (4 - sec)
        print("\r", "Identifying buildings |", text,
              "| [%d / %d] %.2f%% done  Est: %.2f sec left  %s Identifying section (%d, %d)" % (count, totalCuts, percent * 100, est, loadingText, a, b), end="", sep="")
        a += 1
    b += 1
    a = 0

print("\r", "Finished identifying buildings!", sep="")


timeStart = int(time.time() * 1000)
a = 0
b = 0
count = 0
outImg = []
for i in range(21):
    outImg.append(np.copy(img))
for i in range(0, imgheight, CHANGE_SIZE):
    for j in range(0, imgwidth, CHANGE_SIZE):
        count += 1
        cut = img[j: j+width, i: i+height, :]
        change = img[j+shrink: j+CHANGE_SIZE+shrink, i+shrink: i+CHANGE_SIZE+shrink, :]
        if cut.shape != (height, width, 3):
            continue
        ndviCut = processimage.calc(change)
        for p in range(21):
            if predictArray[a, b] > (p + 2):
                for w in range(CHANGE_SIZE):
                    for h in range(CHANGE_SIZE):
                        for colors in range(3):
                            outImg[p][j+shrink+w, i+shrink+h, colors] = ndviCut[w, h, colors]
            else:
                for w in range(CHANGE_SIZE):
                    for h in range(CHANGE_SIZE):
                        for colors in range(3):
                            outImg[p][j+shrink+w, i+shrink+h, colors] = 255
        if True:
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
                  "| [%d / %d] %.2f%% done  Est: %.2f sec left  %s Processing section (%d, %d)" % (count, totalCuts, percent*100, est, loadingText, a, b), end="", sep="")
        a += 1
    b += 1
    a = 0

print("\r", "Done processing image!", sep="")

for p in range(21):
    aa = outImg[p][shrink:-shrink, shrink:-shrink, :]
    cv2.imwrite("output/out-%d.jpg" % p, aa)
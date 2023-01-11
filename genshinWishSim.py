import random

fiveStarRate = 6
fourStarRate = 51

softPityFive = 74
softPityFour = 9

pityFive = 90
pityFour = 10

pricePerPull = 160

rateUpFive = ["eula"]
standardFive = ["mona", "keqing", "qiqi", "diluc", "jean"]

rateUpFour = ["xinyan", "xingqiu", "beidou"]
standardCharFour = ["rosaria", "sucrose", "diona", "chongyun", "noelle", "bennett", "fischl", "ningguang", "xiangling",
                    "razor", "barbara"]
standardWeaponFour = ["rust", "sacrificial bow", "the stringless", "favounius warbow", "eye of perception", "sacrificial fragments",
                      "the widsith", "favounius codex", "favounius lance", "dragon's bane", "rainslasher", "sacrificial greatsword",
                      "the bell", "favounius greatsword", "lions roar", "sacrificial sword", "the flute", "favounius sword"]
standardThree = ["slingshot", "sharpshooter's oath", "raven bow", "emerald orb", "dragon slayers", "magic guide", "black tassel",
                 "debate club", "bloodtained greatsword", "ferrous shadow", "skyrider sword", "harbinger of dawn", "cool steel"]


def chooseRandItem(list):
    return list[random.randint(0, len(list) - 1)]


def initList(pList, pool):
    for i in pool:
        pList[i] = 0


auto = True
autoPulls = 465

pullToFive = 0
lastFiveRateUp = True
pullToFour = 0
lastFourRateUp = True

pullList = {}

initList(pullList, rateUpFive)
initList(pullList, standardFive)
initList(pullList, standardCharFour)
initList(pullList, rateUpFour)
initList(pullList, standardWeaponFour)
initList(pullList, standardThree)

masterlessStarglitter = 0
masterlessStardust = 0

totalPulls = 0
totalFive = 0
totalFour = 0

fourMessage = False
fiveMessage = False

gotFiveList = [0] * 90
gotFourList = [0] * 15

while True:
    if auto:
        if totalPulls >= autoPulls:
            print("Pull done!")
            break
        else:
            if totalPulls % 500000 == 0 and totalPulls > 0:
                print("Done %d pulls out of %d pulls (%f%%)" % (totalPulls, autoPulls, totalPulls / autoPulls * 100))
            pulls = 100
    else:
        pulls = int(input("Number of pulls: "))
        if pulls == 0:
            print("Pull done!")
            break
    for i in range(pulls):
        luck = random.randint(1, 1000)
        totalPulls += 1
        pullToFive += 1
        pullToFour += 1
        luckFive = fiveStarRate if pullToFive < softPityFive else min(round(fiveStarRate + 1000 / (pityFive - softPityFive + 1) * (pullToFive - softPityFive + 1)), 1000)
        luckFour = fourStarRate if pullToFour < softPityFour else min(round(fourStarRate + 1000 / (pityFour - softPityFour + 1) * (pullToFour - softPityFour + 1)), 1000)
        #luckFive = fiveStarRate if pullToFive < softPityFive else round(fiveStarRate + (1000 - fiveStarRate) / (pityFive - softPityFive + 1) * (pullToFive - softPityFive + 1))
        #luckFour = fourStarRate if pullToFour < softPityFour else round(fourStarRate + (1000 - fourStarRate) / (pityFour - softPityFour + 1) * (pullToFour - softPityFour + 1))
        if luck <= luckFive or pullToFive >= 90:
            totalFive += 1
            gotFiveList[pullToFive - 1] += 1
            rateUp = False if random.randint(1, 2) == 1 else True
            if not lastFiveRateUp or rateUp:
                pullList[rateUpFive[0]] += 1
                if fiveMessage:
                    print("You got %s in %d pulls!" % (rateUpFive[0], pullToFive))
                if pullList[rateUpFive[0]] >= 8:
                    masterlessStarglitter += 25
                elif pullList[rateUpFive[0]] >= 2:
                    masterlessStarglitter += 10
                lastFiveRateUp = True
            else:
                gotChar = chooseRandItem(standardFive)
                pullList[gotChar] += 1
                if fiveMessage:
                    print("You got %s in %d pulls!" % (gotChar, pullToFive))
                if pullList[gotChar] >= 8:
                    masterlessStarglitter += 25
                elif pullList[gotChar] >= 2:
                    masterlessStarglitter += 10
                lastFiveRateUp = False
            pullToFive = 0
        elif luck <= luckFive + luckFour or pullToFour >= 10:
            totalFour += 1
            rateUp = False if random.randint(1, 2) == 1 else True
            gotFourList[pullToFour - 1] += 1
            if not lastFourRateUp or rateUp:
                gotChar = chooseRandItem(rateUpFour)
                pullList[gotChar] += 1
                if fourMessage:
                    print("You got %s in %d pulls!" % (gotChar, pullToFour))
                if pullList[gotChar] >= 8:
                    masterlessStarglitter += 10
                elif pullList[gotChar] >= 2:
                    masterlessStarglitter += 2
                lastFourRateUp = True
            elif random.randint(1, 2) == 1:
                gotChar = chooseRandItem(standardCharFour)
                pullList[gotChar] += 1
                if fourMessage:
                    print("You got %s in %d pulls!" % (gotChar, pullToFour))
                if pullList[gotChar] >= 8:
                    masterlessStarglitter += 5
                elif pullList[gotChar] >= 2:
                    masterlessStarglitter += 2
                lastFourRateUp = False
            else:
                gotChar = chooseRandItem(standardWeaponFour)
                pullList[gotChar] += 1
                if fourMessage:
                    print("You got %s in %d pulls!" % (gotChar, pullToFour))
                masterlessStarglitter += 2
                lastFourRateUp = False
            pullToFour = 0
        else:
            gotChar = chooseRandItem(standardThree)
            pullList[gotChar] += 1
            masterlessStardust += 15

print("In %d pulls" % totalPulls)
print("Got %d %s" % (pullList["eula"], "eula"))
#for items, number in pullList.items():
    #print("Got %d %s" % (number, items))

getFiveRate = round(totalFive / totalPulls * 100, 4)
getFourRate = round(totalFour / totalPulls * 100, 4)
print("Five star rate: %f%%" % getFiveRate)
print("Four star rate: %f%%" % getFourRate)
print("Got %d starglitters and %d stardusts" % (masterlessStarglitter, masterlessStardust))
print("Wasted %d primogems" % (pricePerPull * totalPulls))
print("Costs %d USD" % (round(pricePerPull * totalPulls / 8080 * 99.99)))
print("---------------------------------------------")

#for i in range(len(gotFiveList)):
#    print("{:4s} {:6.4f}%    ".format(str(i + 1) + ":", round(gotFiveList[i] / totalFive * 100, 4)), end="")
#    if i % 5 == 4:
#        print("\n", end="")
#print("---------------------------------------------")
#for i in range(len(gotFourList)):
#    print("{:4s} {:6.4f}%    ".format(str(i + 1) + ":", round(gotFourList[i] / totalFour * 100, 4)), end="")
#    if i % 5 == 4:
#        print("\n", end="")

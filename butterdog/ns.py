import requests
from bs4 import BeautifulSoup
import random

number = 122345
resa = requests.get("https://nhentai.net/")
soupa = BeautifulSoup(resa.text, "html.parser")
lnk = soupa.find_all("a", {"class": "cover"})
#bigNum = int(lnk[5]["href"].split("/")[2])

def findRandHen():
    numIn = random.randint(1, 300000)
    return findHen(numIn)


def findHen(num):
    res = requests.get("https://nhentai.net/g/" + str(num) + "/")
    soup = BeautifulSoup(res.text, "html.parser")
    tagType = soup.find_all("span", {"class": "tags"})
    allTagName = soup.find_all("span", {"class": "name"})
    title = soup.find_all("span", {"class": "pretty"})
    tagName = ["Parodies", "Characters", "Tags", "Artists", "Groups", "Languages", "Categories", "Pages"]
    outTitle = []
    for i in title:
        outTitle.append(i.string)
    if len(tagType) != 0:
        tagTypeNum = []
        for i in tagType:
            tagTypeNum.append(int(str(i).count("tag-")))
        tagTypeNum.pop()
        tagTypeNum.pop()
        out = []
        count = 0
        for i in tagTypeNum:
            temp = []
            for j in range(i):
                temp.append(allTagName[count].string)
                count += 1
            out.append(temp)
        ret = []
        ret.append("Title: " + " / ".join(outTitle))
        for i in range(len(out)):
            if tagTypeNum[i] == 0:
                continue
            ret.append("{:s}: {:s}".format(tagName[i], " / ".join(out[i])))
        ret.append("https://nhentai.net/g/" + str(num) + "/")
        return ret
    else:
        a = ["No hentai found"]
        return a

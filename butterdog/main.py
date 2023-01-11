import discord
import random
import requests
import datetime
import time
import asyncio
from discord.ext import tasks
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
import ns

dictionary = []
jamesID = "457266670281556010"
ericID = "518747365717573632"
aliceID = "728717623168073810"
beeScript = []
beeNum = 0
for line in open("words_list.txt"):
    dictionary.append(line.rstrip().split())
print("DICTIONARY PREPARED")
for line in open("gistfile1.txt"):
    stripLine = line.rstrip()
    if not line.isspace():
        beeScript.append(stripLine)
print("BEE MOVIE PREPARED")
potass = ""
for line in open("potass.txt"):
    potass += line
genshintxt = ""
for line in open("genshin.txt"):
    genshintxt += line
sustxt = []
for line in open("sus.txt"):
    stripLine = line.rstrip()
    sustxt.append(stripLine)
sustext = "\n".join(sustxt)
print("Other ready yay")
beeStart = False
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

client = discord.Client()
spam = {}
lastSpam = {}



@tasks.loop(seconds=5.0)
async def spamDetect():
    global lastSpam
    for i in spam:
        if i in lastSpam:
            if spam[i] == lastSpam[i]:
                spam[i] = 0
    lastSpam = spam.copy()





@client.event
async def on_ready():
    global butterdogDiscord, jamesRole
    await client.wait_until_ready()
    butterdogDiscord = client.get_guild(811159694408286228)
    jamesRole = butterdogDiscord.get_role(811581274069270529)
    print("-----------------------------------")
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global beeStart, nowAt, beeNum
    if message.author == client.user:
        return

    if message.channel.id == 896061039710457898:
        return

    print(message.content)
    if message.content.startswith('<:'):
        return

    msg = message.content
    lowermsg = message.content.lower()
    upmsg = message.content.upper()

    # STOP BOT

    if msg == "a$stop$":
        await message.channel.send("logging out")
        await client.logout()
        return

    # DETECT SPAM

    if message.author.id not in spam:
        spam[message.author.id] = 1
    else:
        spam[message.author.id] += 1

    for i in spam:
        if spam[i] > 10 and i == message.author.id:
            sendmsg = []
            await message.delete()
            if random.randint(1, 5) == 1:
                for j in range(3):
                    sendmsg.append("<@" + str(message.author.id) + "> WHY YOU SPAM SPAM NO GOOD!")
                    sendmsg.append("<@" + str(message.author.id) + "> STOP SPAMMING YOU IDIOT!")
                sendmsg.append("Please send another message after 10 seconds so no spam thanks!!!!!")
                await message.channel.send("\n".join(sendmsg))
            return

    # NO MENTION

    if client.user in message.mentions:
        sentUser = message.author.id
        sendmsg = []
        for i in range(5):
            sendmsg.append("<@" + str(sentUser) + "> WHAT OMG DONT MENTION ME")
        await message.channel.send("\n".join(sendmsg))
        return


    # BEE MOVIE

    if "bee" in lowermsg:
        await message.channel.send(beeScript[beeNum])
        beeNum = 0 if beeNum >= len(beeScript) - 1 else beeNum + 1

    # MOM
    if "mom" in lowermsg:
        if "ur" in lowermsg:
            await message.channel.send("<@" + str(message.author.id) + "> STOP SAYING MY MOM OR ILL DO YOUR MOM")
        else:
            await message.channel.send("ur mom")

    # GENSHIN

    if "genshin" in lowermsg:
        await message.channel.send(genshintxt)

    # NITRO

    if "nitro" in lowermsg:
        await message.channel.send(file=discord.File('discordNitro.png'))

    # ADD ROLE

    if lowermsg == "$role":
        if message.author not in jamesRole.members and message.author.id == int(jamesID):
            await message.author.add_roles(jamesRole)

    # K
    if lowermsg == "k":
        await message.channel.send(potass)


    # BUTTER DOG MACHINE

    if message.content.startswith('$bd'):
        a = msg.split()
        if len(a) < 3:
            await message.channel.send('INVALD SYNTAX OMG!')
            await message.channel.send('SYNTAX: $bd [spaces] [text]')
        elif a[1].isnumeric():
            spaces = int(a[1])
            txt = " ".join(a[2:])
            total = spaces * 3 - 12 + len(txt)
            allmsg = []
            s = round(spaces / 6)
            for i in range(spaces):
                msgsend = " "
                for j in range(i):
                    if j < s or j >= spaces - s:
                        msgsend += " "
                    elif j < s * 2 or j >= spaces - s * 2:
                        msgsend += "  "
                    else:
                        msgsend += "   "
                msgsend = msgsend[:-1] + "*" + txt + "*"
                msgsend += " " * (total - len(msgsend))
                allmsg.append(msgsend)
            bufferMes = "\n".join(allmsg)
            if len(bufferMes) > 1000:
                await message.channel.send("MESSAGE TOO LONG STOOPID")
            for i in range(spaces):
                msgsend = " "
                for j in range(spaces, i, -1):
                    if j <= s or j > spaces - s:
                        msgsend += " "
                    elif j <= s * 2 or j > spaces - s * 2:
                        msgsend += "  "
                    else:
                        msgsend += "   "
                msgsend = msgsend[:-1] + "*" + txt + "*"
                msgsend += " " * (total - len(msgsend))
                allmsg.append(msgsend)
            await message.channel.send("\n".join(allmsg))
        else:
            await message.channel.send('INVALD SYNTAX OMG!')
            await message.channel.send('SEE INFO STOOPID')

    # JAMES WANT STUFF

    if "uwu" in lowermsg:
        await message.channel.send("owo")
    elif "owo" in lowermsg:
        await message.channel.send("uwu")

    if "ok" == lowermsg:
        await message.channel.send("<@" + str(message.author.id) + "> k")

    if message.content == upmsg and len(message.attachments) < 1 & upmsg.isupper():
        try:
            await message.channel.send("<@" + str(message.author.id) + "> dont do all caps please be polite thank you")
        except:
            await message.channel.send("dont do all caps please be polite thank you")

    if "sus" in lowermsg:
        if random.randint(1, 3) <= 2:
            await message.channel.send(sustext)
        else:
            await message.channel.send("u sussy baka")

    if "bruh" in lowermsg:
        await message.channel.send("bruh")

    if "jam" in lowermsg:
        await message.channel.send("<@" + jamesID + "> jam someone mentioned you! you should have a look!")

    # RANDOM WORD

    if message.content.startswith('$rw'):
        a = msg.split()
        if len(a) != 2:
            await message.channel.send('INVALD SYNTAX OMG!')
            await message.channel.send('SEE INFO STOOPID')
        else:
            search = a[1]
            res = []
            alpha = "abcdefghijklmnopqrstuvwxyz"
            for word in dictionary[alpha.index(search[0])]:
                if word.startswith(search):
                    res.append(word)
            if len(res) == 0:
                await message.channel.send("NO WORD YOU STOOPID")

    # SEARCH FUNCTION

    if message.content.startswith("$what"):
        a = msg.split()
        if len(a) < 2:
            await message.channel.send('INVALD SYNTAX OMG!')
            await message.channel.send('SEE INFO STOOPID')
        else:
            word = "_".join(a[1:])
            await message.channel.send("https://en.wikipedia.org/wiki/" + word)
            await message.channel.send("https://www.google.com/search?q=" + "+".join(a[1:]))

    # YES NO SPAM

    if lowermsg == "yes":
        if random.randint(1, 142) == 23:
            await message.channel.send("ok you win are you happy!???!?")
        else:
            await message.channel.send("no")
    elif lowermsg == "no":
        if random.randint(1, 142) == 21:
            await message.channel.send("ok you win are you happy!???!?")
        else:
            if random.randint(1, 3) == 2:
                await message.channel.send("no u")
            else:
                await message.channel.send("yes")
    elif lowermsg == "no u":
        await message.channel.send("stfu ur mom")

    # THANK AND KICK JAMES

    if "thanks" in lowermsg or "ty" in lowermsg:
        await message.channel.send("<@" + str(message.author.id) + ">your welcome")


    if "thx" in lowermsg:
        sentUser = message.author.id
        await message.channel.send("<@" + str(sentUser) + "> use thanks or ty YOU STOOPID")
        await message.channel.send("bruh")

    if "thank" in lowermsg and "you" not in lowermsg and "thanks" not in lowermsg:
        sentUser = message.author.id
        await message.channel.send("<@" + str(
            sentUser) + "> ITS THANK\"S\" OMG WHY YOU SO STOOPID IM AM SINGULAR NEED S GO LEARN YOUR STUPID GRAMMAR BRUH")

    if jamesID in lowermsg:
        await message.channel.send("<@" + jamesID + "> someone tagged you")

    # JAMES REPLY

    if message.author.id == int(jamesID):
        if "http" in lowermsg and "discord" not in lowermsg:
            if random.randint(1, 10) > 1:
                await message.delete()
                print("message removed lol")
        elif random.randint(1, 15) <= len(lowermsg.split()):
            await message.channel.send("NO MESSAGE FOR JAMES!")
            await message.delete()

    elif message.author.id == int(ericID):
        if random.randint(1, 7) == 3:
            await message.channel.send("wow eric")

    # YOUTUBE

    if lowermsg.startswith("$yt"):
        a = msg.split()
        if len(a) < 2:
            await message.channel.send("USE CORRECT SYNTAX OMG!!!?!?!?!")
        else:
            toSearch = "+".join(a[1:])
            await message.channel.send("https://www.youtube.com/results?search_query=" + toSearch)

    if lowermsg.startswith("nh"):
        a = lowermsg.split()
        if len(a) == 2 and a[1].isdigit():
            henres = ns.findHen(int(a[1]))
            await message.channel.send("\n".join(henres))
        else:
            await message.channel.send("e")

    elif lowermsg == "rndnh":
        henres = ns.findRandHen()
        await message.channel.send("\n".join(henres))



spamDetect.start()
client.run("ODExMTU3MTg3MTQ5MDM3NTY4.GPL23t.5REMUwj_uHhAUaDPd-oAOmLl9kR3iOJ1Y-7t-0")

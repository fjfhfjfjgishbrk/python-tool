import discord
import os
import random

client = discord.Client()

@client.event
async def on_ready():
  print("-----------------------------------")
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
  msg = message.content
  lowermsg = message.content.lower()

  if "luke" in lowermsg:
    await message.channel.send("no u haha")
    return

  if "13" in lowermsg or "thirteen" in lowermsg:
    await message.channel.send("@everyone" + " bruh its 15")

  if "15" in lowermsg or "james" in lowermsg or "fifteen" in lowermsg:
    await message.channel.send("@everyone number 15")
    for i in range(4):
      await message.channel.send("BURGER KING FOOT LETTUCE")
  elif "51" in lowermsg:
    await message.channel.send("did you mean THIRTEEN?")

  if "eric" in lowermsg:
    await message.channel.send("@everyone")
    smsg = message.author.name + " sent ERIC OMG @everyone"
    for i in range(5):
      await message.channel.send(smsg)

  if "invite" in lowermsg:
    for i in range(5):
      await message.channel.send("@everyone ERIC INVITE MY BOT AHHHH")

  if message.mention_everyone:
    await message.channel.send("Ill help you @everyone yay")
    for i in range(random.randint(10, 20)):
      await message.channel.send("*ERIC* @everyone *ERIC*")

  if message.content.startswith('hi'):
    alpha = "abcdefghijklmnopqrstuvwxyz"
    for i in range(5):
      sendmsg = "hi @everyone "
      for j in range(random.randint(15, 25)):
        sendmsg += alpha[random.randint(0, len(alpha) - 1)]
      await message.channel.send(sendmsg)

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
      for i in range(spaces):
        msgsend = "-"
        for j in range(i):
          if j < 2 or j >= spaces - 2:
            msgsend += "-"
          elif j > 5 or j <= spaces - 5:
            msgsend += "--"
          else:
            msgsend += "---"
        msgsend = msgsend[:-1] + "*" + txt + "*"
        msgsend += "-" * (total - len(msgsend))
        allmsg.append(msgsend)
      bufferMes = "\n".join(allmsg)
      if len(bufferMes) > 2000:
        await message.channel.send("MESSAGE TOO LONG STOOPID")
      else:
        await message.channel.send(bufferMes)
      allmsg = []
      for i in range(spaces):
        msgsend = "-"
        for j in range(spaces, i, -1):
          if j <= 2 or j > spaces - 2:
            msgsend += "-"
          elif j >= 5 or j < spaces - 5:
            msgsend += "--"
          else:
            msgsend += "---"
        msgsend = msgsend[:-1] + "*" + txt + "*"
        msgsend += "-" * (total - len(msgsend))
        allmsg.append(msgsend)
      await message.channel.send("\n".join(allmsg))
    else:
      await message.channel.send('INVALD SYNTAX OMG!')
      await message.channel.send('SEE INFO STOOPID')

client.run(os.getenv('TOKEN'))
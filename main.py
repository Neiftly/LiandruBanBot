import discord
import os
import datetime
import time
import requests
import json
import random
import asyncio
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

client = discord.Client()
ENDDATE = datetime.datetime(2021, 7, 20, 15, 4)
STARTDATE = datetime.datetime(2021, 1, 18, 15, 4)
message_channel_id='335154913569013771'
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
good_responses = [
  "Cheer Up!",
  "Hang in There.",
  "You are an OK person / bot"
]
sendtime = '15:04'
bot = commands.Bot(command_prefix='$')

os.environ['TZ'] = 'America/Chicago'
time.tzset()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def get_now():
  time = datetime.datetime.now()
  return time

def update_triggers(triggering_message):
  if "triggers" in db.keys():
    triggers = db["triggers"]
    triggers.append(triggering_message)
    db["triggers"] = triggers
  else:
    db["triggers"] = [triggering_message]

def delete_trigger(index):
  triggers = db["triggers"]
  if len(triggers) > index:
    del triggers[index]
  db["triggers"] = triggers

def update_responses(encouraging_message):
  if "encouragements" in db.keys():
    encouragements =  db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
  
def delete_response(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('Liandru Ban Bot is logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send('Hello!')

  if msg.startswith('$sentence'):
    await message.channel.send(ENDDATE.strftime('%A %B %d %Y at %I:%M%p Server Time'))

  if msg.startswith('$freedom'):
    y =  get_now()
    z = (ENDDATE - y)
    if ENDDATE < y:
      await message.channel.send('He is Free!')
    else:
      await message.channel.send(str(z.days) + ' days left until Liandru can fish again.')
  
  if msg.startswith('$timeserved'):
    y =  get_now()
    z = -1*(STARTDATE - y)
    if ENDDATE < y:
      await.message.channel.send('6 Months were served!')
    else:
      await message.channel.send(str(z.days) + ' days have been served')

  if msg.startswith('$damage'):
    await message.channel.send('You should have used FEINT!')
    await message.channel.send('https://www.wowhead.com/spell=1966/feint')

  if msg.startswith('$extra'):
    await message.channel.send('This is the Liandru Botting Ban Bot!')
    await message.channel.send('On ' + STARTDATE.strftime('%A %B %d %Y at %I:%M%p Server Time') + 'Liandru was Banned until '  + ENDDATE.strftime('%A %B %d %Y at %I:%M%p Server Time'))
    await message.channel.send('You might be wondering, why? Well he decided that fishing was too mindnumbingly boring so he used a bot for 30 minutes to catch the cheapest fish on the auction house.')
    await message.channel.send('This bot was created to help the guild taunt Liandru')
    await message.channel.send('If you wish to add more commands contact Neift')
    await message.channel.send('Thanks for Using the Liandru Ban Bot!')

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = good_responses
  if "encouragements" in db.keys():
    options = options + db["encouragements"]
  
  sadness = sad_words
  if "triggers" in db.keys():
    sadness = sadness +  db["triggers"]

  if any(word in msg for word in sadness):
    await message.channel.send(random.choice(options))

  if msg.startswith("$newBad"):
    triggering_message = msg.split("$newBad", 1)[1]
    update_triggers(triggering_message)
    await message.channel.send("New Trigger Added.")

  if msg.startswith("$newGood"):
    encouraging_message = msg.split("$newGood", 1)[1]
    update_responses(encouraging_message)
    await message.channel.send("New Encouraging Message Added.")

  if msg.startswith("$delBad"):
    triggers = []
    if "triggers" in db.keys():
      index = int(msg.split("$delBad", 1)[1])
      delete_trigger(index)
      triggers = db["triggers"]
    await message.channel.send(triggers)

  if msg.startswith("$delGood"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$delGood", 1)[1])
      delete_response(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$listBad"):
    triggers = sad_words
    if "triggers" in db.keys():
      triggers = triggers + db["triggers"]
    await message.channel.send(triggers)

  if msg.startswith("$listGood"):
    encouragements = good_responses
    if "encouragements" in db.keys():
      encouragements = encouragements + db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$responding"):
    value = msg.split("responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")

    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

  if msg.startswith("$info"):
    await message.channel.send('This is the Liandru Botting Ban Bot!')
    await message.channel.send('All commands start with $')
    await message.channel.send('Commands Include: hello, sentence, freedom, timeserved, damage, inspire, newGood, newBad, delGood, delBad, listGood, listBad, responding, and extra')


keep_alive()
client.run(os.getenv('TOKEN'))
import asyncio
import json
import os
from functools import partial
from typing import Any
import BenBotAsync
import aiohttp
import crayons
import discord
import fortnitepy
import requests
from discord.ext import commands
from datetime import datetime, date
from EpicEndpoints import EpicEndpoints

website = "https://atomicxyz.tk/atomicbot/"
tutorial = "https://youtu.be/Mo1p69GGuas"
lobbybot_commands = "**Cosmetic Commands**\na!skin `name` - Changes the bot's skin\na!emote `name` - Changes the bot's emote\na!backpack `name` - Changes the bot's backbling\na!pickaxe `name` - Changes the bot's pickaxe\na!level `number` - Changes the bot's level\na!style `cosmetic name` - Changes the style/variant of a cosmetic\na!hide/a!unhide - Hides and unhides the bot's party members\na!pinkghoul - Changes to the pink ghoul trooper skin\na!purpleskull - Changes to the purple skull trooper skin\na!cid/eid/pid/bid `id` - Changes the bot's cosmetic by cosmetic ID\n\n**Utility Commands**\na!ready/a!unready - Changes the bot to the ready/unready state\na!say `message` - Makes the bot send a message to party\na!privacy `public/private` - Changes the bot's party privacy\na!sitin/a!sitout - Makes the bot sit in or sit out\na!match/a!unmatch - Changes the bot's status to in-match"

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# mydb = myclient['atomicbot_db']

# #SAVING BOTS

# mycol = mydb["user_bots"]

# def getUserBots(user_id):
#   bots = []
#   documents = list(mycol.find())
#   for doc in documents:
#       if(doc['user_id'] == user_id):
#           bots.append(doc)
#   print(bots)
#   return bots

# def storeSavedBot(user_id,auths):
#     client = {"user_id" : user_id, "auths" : auths}
#     mycol.insert_one(client)
#     print(crayons.green("Saved Bot in Database"))

# def getSavedBot(user_id):
#   documents = list(mycol.find())
#   for doc in documents:
#       if(doc['user_id'] == user_id):
#           print(doc['auths'])

# def deleteSavedBot(user_id):
#     mycol.delete_one({'user_id' : user_id})
#     print(f"Deleted {user_id}")


# #CURRENT BOTS MONGODB
# current_bots = mydb['current_bots']
# def storeCurrentBot(user_id,info):
#     # x = {"user_id" : user_id, "client_info" : info}
#     # current_bots.insert_one(x)
#     print(crayons.green("Saved Current UserId/Bot in Database"))

# def deleteCurrentBot(user_id, info):
#     # current_bots.delete_one({'user_id' : user_id, 'client_info' : info})
#     print("Deleted current_bots")

#EPIC GAMES REQUESTS
def getDisplayName(account_id):
  access_token = getAccessToken()

  url = "https://account-public-service-prod.ol.epicgames.com/account/api/public/account/"

  querystring2 = {"accountId":account_id}
  
  headers = {
        'content-type': "application/json",
        'authorization': f"bearer {access_token}",
        'cache-control': "no-cache",
        }

  response = requests.request("GET", url, headers=headers,params=querystring2)

  data = json.loads(response.text)
  print(data)
  return data[0]['displayName']

def getCosmetic(cosmetic):
  try:
    url = "https://api.gummyfn.com/cosmetic/"

    querystring2 = {"name":cosmetic}

    headers = {
        'content-type': "application/ json",
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers,params=querystring2)

    data = json.loads(response.text)
    return data
  except:
    return None

def channelData(data, channel2) -> None:
        for d in data:
          channel = d['channel']
          if(channel == channel2):
            if(channel2 ==  "clothingcolor" or channel2 == "parts"):
              return d['number']-1
            elif(channel2 == "jerseycolor"):
              return d['tag']
            else:
              return d['number']
        return None

def getBR():
    url = "https://fortnite-api.com/v2/news/br"

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers)

    data = json.loads(response.text)

    return data

def getStats(name, device):
    url = "https://fortnite-api.com/v1/stats/br/v2"

    params = {
      "name" : name,
      "accountType" : device,
      "timeWindow" : "lifetime",
      "image" : "all"
    }

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers, params=params)

    data = json.loads(response.text)

    return data['data']

async def getVariants(id):
    try:
      url = f"https://fortnite-api.com/v2/cosmetics/br/search/?id={id}"

      async with aiohttp.ClientSession() as client:
        async with client.get(url=url) as r:
          data = await r.json()

      return data["data"]["variants"]
    except:
      return None

clientToken = "NTIyOWRjZDNhYzM4NDUyMDhiNDk2NjQ5MDkyZjI1MWI6ZTNiZDJkM2UtYmY4Yy00ODU3LTllN2QtZjNkOTQ3ZDIyMGM3"

def getAccessToken():
    url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"

    payload = "grant_type=client_credentials"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'authorization': "basic YjA3MGYyMDcyOWY4NDY5M2I1ZDYyMWM5MDRmYzViYzI6SEdAWEUmVEdDeEVKc2dUIyZfcDJdPWFSbyN+Pj0+K2M2UGhSKXpYUA==",
        'cache-control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    data = json.loads(response.text)

    access_token = data['access_token']
    expire = data['expires_in']

    return access_token

def getDeviceCode(access_token):
    url2 = "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/deviceAuthorization"

    querystring2 = {"prompt":"login"}

    payload2 = "prompt=promptType"
    headers2 = {
        'content-type': "application/x-www-form-urlencoded",
        'authorization': f"bearer {access_token}",
        'cache-control': "no-cache",
        }

    response2 = requests.request("POST", url2, data=payload2, headers=headers2, params=querystring2)

    data2 = json.loads(response2.text)

    return data2

def getDeviceAuth(devicecode):
    url3 = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"

    payload3 = f"grant_type=device_code&device_code={devicecode}"
    headers3 = {
        'content-type': "application/x-www-form-urlencoded",
        'authorization': f"basic {clientToken}",
        'cache-control': "no-cache",
        }

    response3 = requests.request("POST", url3, data=payload3, headers=headers3)

    data3 = json.loads(response3.text)

    return data3

def getIDs(access_token,account_id):
  url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}/deviceAuth"

  headers = {
      'content-type': "application/json",
      'authorization': f"bearer {access_token}",
      'cache-control': "no-cache",
      }

  response = requests.request("POST", url, headers=headers)

  data = json.loads(response.text)

  return data


def getClient(device_id:str,account_id:str,secret:str,message):
    acceptFriend = True
    status = 'AtomicBot by AtomicXYZ'
    platform = 'PSN'
    joinMessage = ''
    client = fortnitepy.Client(auth=fortnitepy.DeviceAuth(
      device_id=device_id,
      account_id=account_id,
      secret=secret,
      ios_token=clientToken
      ),
      status=status,
      platform=fortnitepy.Platform(platform)
    )

    @client.event
    async def event_friend_request(request): 
      try:
        await request.accept()
      except:
        print(crayons.red("Friend Request Error"))

    @client.event
    async def event_party_invite(invitation):
      # embed = discord.Embed(
      #   title=f"This Feature is Currently Down: Party Invites",
      #   color=color)
      # await message.author.send(embed=embed)
      # embed2 = discord.Embed(
      #   title=f"Please Instead Join the Bot's Party and type: \"a!privacy private\"",
      #   color=color)
      # await message.author.send(embed=embed2)
      
      print(f"Invite from {invitation.sender.display_name}\nBot Owner: {message.author.name}")
      try:
        if(invitation.sender):
          embed = discord.Embed(
              title=f"Party Invite From {invitation.sender.display_name}",
              description="Should I Accept the Invite?",
              color=color)
          await asyncio.sleep(1)
          msgEmbed = await message.author.send(embed=embed)
          reactions = ['✅','❌']
          for emoji in reactions: 
            await msgEmbed.add_reaction(emoji)
          
          def check(reaction, user):
            return reaction.message == msgEmbed and user == message.author

          reaction = await bot.wait_for('raw_reaction_add', check=lambda reaction: reaction.message_id == msgEmbed.id and reaction.user_id == message.author.id)

          if reaction.emoji.name == '✅':
            try:
              if(invitation and invitation.sender):
                try:
                  await invitation.accept()
                except(fortnitepy.errors.HTTPException, fortnitepy.errors.Forbidden) as e:
                  print("Error on Accept")
                  pass
                embed = discord.Embed(
                    title=f"Accepted Invite From {invitation.sender.display_name}",
                    color=color)
                msgAccept = await message.author.send(embed=embed)
                await asyncio.sleep(5)
                await msgAccept.delete()
                await asyncio.sleep(1)
                await msgEmbed.delete()
            except:
              embed = discord.Embed(
                  title=f"Error Joining Party",
                  color=color)
              await message.author.send(embed=embed)
              print(crayons.red("Error Joining Party"))
          elif reaction.emoji.name == '❌':
            await invitation.decline()
            embed = discord.Embed(
                  title=f"Declined Invite From {invitation.sender.display_name}",
                  color=color)
            msgDecline = await message.author.send(embed=embed)
            await asyncio.sleep(5)
            await msgDecline.delete()
            await asyncio.sleep(1)
            await msgEmbed.delete()
      except Exception as e:
        print(crayons.red(f"Party Invite Error: {e}"))
        pass
    return client

    

async def edit_and_keep_client_member(self):
  member = self.party.me
  try:
    await member.edit_and_keep(
      partial(member.set_outfit, asset='CID_253_Athena_Commando_M_MilitaryFashion2'),
      partial(member.set_banner, icon="OtherBanner28", season_level=999),
      partial(member.set_emote, asset='EID_Floss',run_for=20),
      partial(member.set_backpack, asset= 'BID_134_MilitaryFashion')
    )
  except:
    print(crayons.red("Error Editing Styles"))
    return

loop = asyncio.get_event_loop()

prefix = 'a!'
prefixs = "a!","A!"

color = 0xff0000
footertext = "AtomicBot v2.5 | By AtomicXYZ"

intents = discord.Intents.default()

bot = commands.Bot(command_prefix=prefixs, intents=intents)

bot.remove_command('help')

class fnAPICosmetic:
  def __init__(self, name, id):
    self.id = id
    self.name = name

async def getFortniteAPI(name):
  try:
    url = f"https://fortnite-api.com/v2/cosmetics/br/search?name={name}"

    async with aiohttp.ClientSession() as client:
      async with client.get(url=url) as response:
        data = await response.json()
    return data
  except:
    return None

async def fetch_cosmetic(type_, name) -> None:
    data = None
    # try:
    #   data = await BenBotAsync.get_cosmetic(
    #           lang="en",
    #           searchLang="en",
    #           matchMethod="full",
    #           name=name,
    #           backendType=type_
    #       )
    # except:
    #     try:
    #       data = await BenBotAsync.get_cosmetic(
    #               lang="en",
    #               searchLang="en",
    #               matchMethod="contains",
    #               name=name,
    #               backendType=type_
    #           )
        # except:
    try:
      APIdata1 = await getFortniteAPI(name)
      APIdata =  APIdata1['data']
      data = fnAPICosmetic(name=APIdata['name'],id=APIdata['id'])
      print("Cosmetic Fetched: " + data.name)
    except:
      data = None
    return data

async def set_and_update_party_prop(self, schema_key: str, new_value: Any) -> None:
    prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

    await self.party.patch(updated=prop)

async def send_shop(channel_id):
  r = requests.get(url="https://fortool.fr/cm/api/v1/shop?lang=en")
  data = json.loads(r.text)
  url = data['images']['default']
  
  today = date.today()
  day2 = today.strftime("%b %d %Y")
  embed = discord.Embed(
    title = "Item Shop for " + day2,
    color=color
  )
  embed.set_image(url=url)
  channel = bot.get_channel(channel_id)
  await channel.send(embed=embed)

botdict = {}
savedauths = {}

def logBots():
  with open('device_auths.json', 'w') as fp:
    json.dump(botdict, fp, sort_keys=False, indent=4)

def getBots():
  with open('device_auths.json', 'w') as fp:
    data = json.load(fp)
  return data

emoteseconds = 60
expiretime = 180
profileimg = "https://cdn.discordapp.com/avatars/829050201648922645/d8d62960d600af3975b61735ccc5e90c.png?size=128"

@bot.event
async def on_ready():
  print(crayons.green('Logged in'))
  while True:
    try:
      today = datetime.utcnow()
      hour = today.strftime("%H %M")
      if(hour == "00 01"):
        await send_shop(803080074396041218)
        hour = "00 02"
        await asyncio.sleep(60)
      await bot.change_presence(activity=discord.Game(name="by AtomicXYZ"))
      await asyncio.sleep(5)
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(bot.guilds)) + " Servers"))
      await asyncio.sleep(5)
      await bot.change_presence(activity=discord.Game(name="a!start for a bot"))
      await asyncio.sleep(5)
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(botdict)} bots online"))
      await asyncio.sleep(5)
    except Exception as e:
      print(e)
      continue

@bot.event
async def on_message(message):
    await asyncio.sleep(1)
    try:
      if message.channel.id == (831968067684007987):
          await message.delete()
    except:
      print('Error Deleting Message')

    msgCont = message.content.lower()
    args = msgCont.split(" ")
    client = botdict.get(message.author.id, None)
    auths = savedauths.get(message.author.id, None)
    end = args[1:]
    command = " ".join(end)
    skinurl = "-".join(end)
    
    if(args[0] == prefix + 'start' or args[0] == prefix + 'startbot'):
        try:
          await message.delete()
        except:
          pass
        await asyncio.sleep(4)
        if(client):
          embed=discord.Embed(
          title="Error: Bot Currently Running",
          description="Stop the bot with " + prefix + "stop, then type " + prefix + "start", 
          color=color)
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return

        access_token = getAccessToken()
        data = getDeviceCode(access_token)

        embed=discord.Embed(
        title="AtomicBot Control Panel",
        description=f"**1.** [**Click Here**](https://epicgames.com/) **and Log in with an ALT Account**\n\n**2.** [**Click Here**]({data['verification_uri_complete']}) **and click \"confirm\"**\n\n**3. React with ✅**\n\n**React with ❌ cancel**",
        color=color)
        embed.set_author(name="AtomicBot",icon_url=profileimg)

        embed.set_footer(text=footertext)

        msgEmbed = await message.author.send(embed=embed)
        reactions = ['✅','❌']
        
        for emoji in reactions: 
          await msgEmbed.add_reaction(emoji)

        reaction = await bot.wait_for('raw_reaction_add', check=lambda reaction: reaction.message_id == msgEmbed.id and reaction.user_id == message.author.id)

        if reaction.emoji.name == '✅':
          try:
            data2 = getDeviceAuth(data['device_code'])
            dataID = getIDs(data2['access_token'],data2['account_id'])
            
            device = dataID['deviceId']
            account = dataID['accountId']
            secret = dataID['secret']

            client = getClient(device, account, secret, message)
          except Exception as e:
            print(f"Bot creation error: {e}")
            await asyncio.sleep(1)
            embed=discord.Embed(
              title="Error: Please complete __Step 2__ and click \"Confirm\" before clicking ✅",
              color=color)
            embed.set_author(name="AtomicBot",icon_url=profileimg)

            embed.set_footer(text=footertext)

            msgEmbed = await message.author.send(embed=embed)
            return

        else:
          print("Bot creation cancelled")
          
          embedcancel=discord.Embed(
            title="Bot Creation Cancelled",
            color=color)
          embedcancel.set_author(name="AtomicBot",icon_url=profileimg)

          embedcancel.set_footer(text=footertext)

          await msgEmbed.edit(embed=embedcancel)
          return
        
        print("Bot Creation Started")
        global tasks

        tasks = []

        try:
          tasks.append(client.start())
          tasks.append(bot.loop.create_task(client.wait_until_ready()))
          done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        except: 
          print("cancelled")
          for task in tasks:
            task.cancel

        if(tasks[1] in done):
          botdict[message.author.id] = client
          client_info = {'name' : client.user.display_name, 'id' : client.user.id}
          # storeCurrentBot(message.author.id, client_info)
          savedauths[message.author.id] = {
            'device_id' : device,
            'account_id' : account,
            'secret' : secret
          }

          print(crayons.green(f'Bot ready as {client.user.display_name}'))
          await edit_and_keep_client_member(client)
          embed = discord.Embed(
            title=f"Bot Control Panel for {client.user.display_name}",
            description=f"**Bot Info**\nYour Bot will expire in **{expiretime} min**\nType **" + prefix + f"stop** to stop your bot\n\n{lobbybot_commands}\na!help - Sends the help message",
            color=color)
          embed.set_thumbnail(url=f"https://benbot.app/cdn/images/{client.party.me.outfit}/icon.png")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          embed2 = discord.Embed(
            title="❗Important",
            description=f"**Watch this video if you need help:** {tutorial}\n**Join the support server:** https://discord.gg/qJqMaTfVK9",
            color=color
          )

          await msgEmbed.delete()
          await message.author.send(embed=embed)
          await message.author.send(embed=embed2)

          await asyncio.sleep(expiretime*60)

          del botdict[message.author.id]
          await client.close(close_http=True,dispatch_close=True)
          if(client.is_closed):
            print(crayons.red(f"Bot cancelled {client.user.display_name}"))
          
          embeddone = discord.Embed(
            title=
            "Bot Expired!",
            description=
            "Restart Bot by typing " + prefix + "start",
            color=color)
          await message.author.send(embed=embeddone)
          return

        else:
          embed = discord.Embed(
            title="Bot was unable to start!",
            description="You can create a new bot with " + prefix + "start",
            color=color)
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
    try:
      # if(args[0] == prefix + 'save'):
      #   if(auths):
      #     embed=discord.Embed(
      #       title="Would you like to save this bot?",
      #       description=f"**React with ✅ to save the bot**\n\n**React with ❌ cancel**",
      #       color=color)
      #     embed.set_author(name="AtomicBot",icon_url=profileimg)

      #     embed.set_footer(text=footertext)

      #     msgEmbed = await message.author.send(embed=embed)
      #     reactions = ['✅','❌']
          
      #     for emoji in reactions: 
      #       await msgEmbed.add_reaction(emoji)
          
      #     def check(reaction, user):
      #       return reaction.message == msgEmbed and user == message.author

      #     reaction = await bot.wait_for('raw_reaction_add', check=lambda reaction: reaction.message_id == msgEmbed.id and reaction.user_id == message.author.id)
      #     try:
      #       if reaction.emoji.name == '✅':
      #         storeSavedBot(message.author.id, auths)
      #         embed=discord.Embed(
      #         title="Bot Successfully Saved ✅",
      #         color=color)
      #         embed.set_author(name="AtomicBot",icon_url=profileimg)
      #         await message.author.send(embed=embed)
      #       elif(len(getUserBots(message.author.id)) >= 3):
      #         embed=discord.Embed(
      #           title="Error: You currently have the max amount of bots saved",
      #           color=color)
      #         embed.set_author(name="AtomicBot",icon_url=profileimg)
      #         embed.set_footer(text=footertext)
      #         await message.author.send(embed=embed)
      #         return
      #     except Exception as e:
      #       print(e)
      #       pass
      #   else:
      #     embed=discord.Embed(
      #       title="An Error Occurred with Saving Your Bot",
      #       color=color)
      #     embed.set_author(name="AtomicBot",icon_url=profileimg)
      #     embed.set_footer(text=footertext)
      #     await message.author.send(embed=embed)
      
      # if(args[0] == prefix + 'load'):
      #   if(getUserBots(message.author.id)):
      #     if(client):
      #       embed=discord.Embed(
      #         title="You already have a client running, would you like to cancel it and load a new bot?",
      #         description=f"**React with ✅ to load a new bot**\n\n**React with ❌ cancel**",
      #         color=color)
      #       embed.set_author(name="AtomicBot",icon_url=profileimg)

      #       embed.set_footer(text=footertext)

      #       msgEmbed = await message.author.send(embed=embed)
      #       reactions = ['✅','❌']
            
      #       for emoji in reactions: 
      #         await msgEmbed.add_reaction(emoji)
            
      #       def check(reaction, user):
      #         return reaction.message == msgEmbed and user == message.author

      #       reaction = await bot.wait_for('raw_reaction_add', check=lambda reaction: reaction.message_id == msgEmbed.id and reaction.user_id == message.author.id)

      #       try:
      #         if reaction.emoji.name == '✅':
      #           del botdict[message.author.id]
      #           client_info = {'name' : client.user.display_name, 'id' : client.user.id}
      #           deleteCurrentBot(message.author.id, client_info)
      #           for task in tasks:
      #             task.cancel
      #           await client.close(close_http=True,dispatch_close=True)
      #           if(client.is_closed):
      #             print(crayons.red(f"Bot cancelled {client.user.display_name}"))
      #         else:
      #           return
      #       except Exception as e:
      #         print(e)
      #         pass
          
      #     botsString = ""
      #     count = 1
      #     for i in getUserBots(message.author.id):
      #       list_id = i['auths']
      #       account_id = list_id[1]
      #       print(account_id)
      #       user_name = getDisplayName(str(account_id))
      #       botsString += f"{count}. " + user_name + "\n"
      #       count += 1
          
      #     print(botsString)
          
      #     embed=discord.Embed(
      #       title=f"Saved Bots for {message.author.name}",
      #       description=botsString,
      #       color=color)
      #     embed.set_author(name="AtomicBot",icon_url=profileimg)
      #     embed.set_footer(text=footertext)
      #     loadmsg = message.author.send(embed=embed)
      #     nums = ['1️⃣','2️⃣','3️⃣']
      #     for i in range(len(getUserBots(message.author.id))):
      #       loadmsg.add_reaction(nums[i])
          
      #   else:
      #     embed=discord.Embed(
      #       title="You have no bots saved!",
      #       description="Save a bot with **" + prefix + "save** while you have a bot running",
      #       color=color)
      #     embed.set_author(name="AtomicBot",icon_url=profileimg)
      #     embed.set_footer(text=footertext)
      #     await message.author.send(embed=embed)
      #     return

      if(args[0] == '+list'):
        current_list = botdict.items()
        for i in current_list:
          print(i)
      
      if(args[0] == '+send_update'):
        print(command)
        botdict1 = botdict
        for j in botdict1.keys():
          print(j)
          i = await bot.fetch_user(j)
          try:
            await i.send(command)
            print("update notice sent")
          except Exception as e:
            print(f"update notice error: {e}")
            continue
          await asyncio.sleep(1)

      if(args[0] == prefix + 'help'):
        general_commands = f"a!news - Shows the current battle royale news\na!stats `epic games username` - Shows the stats of a player\na!shop - Shows the daily item shop\na!invite - Sends the invite link of the bot\na!help - Sends this message\n\n**Tutorial:** {tutorial}\n**Support Server:** https://discord.gg/qJqMaTfVK9\n**Website:** {website}"
        if(client):
          embed = discord.Embed(
            title=f"Help Page",
            description=f"{lobbybot_commands}\n\n**General Commands**\n{general_commands}",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          
          await message.author.send(embed=embed)

          return
        else:
          embed = discord.Embed(
            title=f"AtomicBot Help",
            description=f"**Create a bot to see the full commands!**\n{general_commands}",
            color=color
          )
          embed.set_thumbnail(url="https://media.discordapp.net/attachments/836446331992145950/836719691459461180/AtomicLogo.png")
        
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          
          await message.channel.send(embed=embed)
          return
    
      if(args[0] == prefix + 'stop' or args[0] == prefix + 'stopbot'):
        if(client):
          del botdict[message.author.id]
          await client.close(close_http=True,dispatch_close=True)
          if(client.is_closed):
            print(crayons.red(f"Bot cancelled {client.user.display_name}"))
          
          embeddone = discord.Embed(
            title=
            "Bot Cancelled!",
            description=
            "Restart Bot by typing " + prefix + "start",
            color=color)
          await message.author.send(embed=embeddone)
        else:
          embeddone = discord.Embed(
            title=
            "You dont have a bot running!",
            description=
            "Start a Bot by typing " + prefix + "start",
            color=color)
          await message.author.send(embed=embeddone)
        return

      if(args[0] == prefix + 'skin'):
        cosmetic = await fetch_cosmetic('AthenaCharacter', command)
        member = client.party.me
        try:
          await member.set_outfit(
            asset=cosmetic.id,
            variants = None
          )
          embed = discord.Embed(
            title="Skin Successfully Changed to " + cosmetic.name,
            description=cosmetic.id,
            color=color
          )
          await asyncio.sleep(1)
          try:
            embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{member.outfit}/icon.png")
            # embed.set_thumbnail(url=f"https://benbot.app/cdn/images/{member.outfit}/icon.png")
          except:
            embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/fortnite_gamepedia/images/b/bb/Fortnite-T_Placeholder_Item_Outfit.png/revision/latest/scale-to-width-down/256?cb=20200722180525")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Skin/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
      
      if(args[0] == prefix + 'cid'):
        member = client.party.me
        try:
          await member.set_outfit(
            asset=args[1],
            variants = None
          )
          embed = discord.Embed(
            title="Skin Successfully Changed",
            description=member.emote,
            color=color
          )
          await asyncio.sleep(1)
          try:
            embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{member.outfit}/icon.png")
            # embed.set_thumbnail(url=f"https://benbot.app/cdn/images/{member.outfit}/icon.png")
          except:
            embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/fortnite_gamepedia/images/b/bb/Fortnite-T_Placeholder_Item_Outfit.png/revision/latest/scale-to-width-down/256?cb=20200722180525")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Skin/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
      
      if(args[0] == prefix + 'pickaxe'):
        cosmetic = await fetch_cosmetic('AthenaPickaxe', command)
        member = client.party.me
        try:
          await member.set_pickaxe(
            asset=cosmetic.id,
          )
          embed = discord.Embed(
            title="Pickaxe Successfully Changed to " + cosmetic.name,
            description=cosmetic.id,
            color=color
          )
          await asyncio.sleep(1)
          try:
            embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{member.pickaxe}/icon.png")
            # embed.set_thumbnail(url=f"https://benbot.app/cdn/images/{member.pickaxe}/icon.png")
          except:
            embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/fortnite_gamepedia/images/b/bb/Fortnite-T_Placeholder_Item_Outfit.png/revision/latest/scale-to-width-down/256?cb=20200722180525")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Pickaxe/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
      
      if(args[0] == prefix + 'pid'):
        member = client.party.me
        try:
          await member.set_pickaxe(
            asset=args[1],
          )
          embed = discord.Embed(
            title="Pickaxe Successfully Changed",
            description=member.pickaxe,
            color=color
          )
          await asyncio.sleep(1)
          try:
            embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{member.pickaxe}/icon.png")
            # embed.set_thumbnail(url=f"https://benbot.app/cdn/images/{member.pickaxe}/icon.png")
          except:
            embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/fortnite_gamepedia/images/b/bb/Fortnite-T_Placeholder_Item_Outfit.png/revision/latest/scale-to-width-down/256?cb=20200722180525")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Pickaxe/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return

      if(args[0] == prefix + 'brnews' or args[0] == prefix + 'news'):
        today = date.today()
        d4 = today.strftime("%b-%d-%Y")
        time = d4.split('-')
        d = ""
        d+=time[0] + " "
        d+=time[1] + ", "
        d+=time[2]
        img = getBR()['data']['image']
        embed = discord.Embed(
            title="Battle Royale News for " + d,
            color=color
        )
        embed.set_image(url=img)
        embed.set_author(name="AtomicBot",icon_url=profileimg)
        embed.set_footer(text=footertext)
        await message.channel.send(embed=embed)
        return
      
      if(args[0] == prefix + 'stats'):
        name = getStats(command,"epic")['account']['name']
        img = getStats(command,"epic")['image']
        await message.channel.send(img)
        return

      if(args[0] == prefix + 'shop'):
        await send_shop(message.channel.id)
        return

      if(args[0] == prefix + 'search'):
        try:
          data1 = await getFortniteAPI(command)
          
          data = data1['data']
          
          embed = discord.Embed(
            title=data['name'],
            description=data['id'],
            color=color
          )
          embed.add_field(
            name="Description",
            value=data['description'],
            inline=False
          )
          try:
            embed.set_thumbnail(url=data['images']['icon'])
          except:
            embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/fortnite_gamepedia/images/b/bb/Fortnite-T_Placeholder_Item_Outfit.png/revision/latest/scale-to-width-down/256?cb=20200722180525")
          embed.set_footer(text=footertext)
          await message.channel.send(embed=embed)
          return
        except Exception as e:
          embed = discord.Embed(
          title="Error: Search Failed",
          description=e,
          color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.channel.send(embed=embed)
          return
      
      if(args[0] == prefix + 'style' or args[0] == prefix + 'styles' or args[0] == prefix + 'variant' or args[0] == prefix + 'variants'):
        if(client):
          cosmetic = await fetch_cosmetic('AthenaCharacter', command)
          variants_full = await getVariants(cosmetic.id)
          count_one = 1
          chosen_variants = []
          for variants in variants_full:
            options = variants["options"]
            try:
              if(options == None):
                embed = discord.Embed(
                title="There are no styles for that skin",
                color=color
                )
                await message.author.send(embed=embed)
                return
              else:
                embed = discord.Embed(
                  title=f"Styles for " + cosmetic.name + f" (Page {count_one})",
                  color=color
                )
                await message.author.send(embed=embed)
                count = 1
                
                for style in options:
                  name = style['name']
                  img = style['image']
                  embed2 = discord.Embed(
                    title=name,
                    description=f"Type {count} to equip",
                    color=color
                  )
                  embed2.set_thumbnail(url=img)
                  await message.author.send(embed=embed2)
                  count += 1
                
                def check(msg):
                  return msg.content and msg.author.id == message.author.id

                msg = await bot.wait_for('message', check=check)
                member = client.party.me
                channel = variants['channel'].lower()
                num2 = int(msg.content)
                style = options[num2-1]
                variantName = style['name']
                thumbnailVar = style['image']
                tag = ""
                try:
                  tag = style['tag']
                except:
                  pass

                variant_obj = {}
                variant_obj['name'] = variantName
                variant_obj['channel'] = channel
                variant_obj['number'] = num2
                variant_obj['image'] = thumbnailVar
                variant_obj['tag'] = tag

                chosen_variants.append(variant_obj)
            except Exception as e:
              embed = discord.Embed(
                title="There are no styles for that skin",
                description=e,
                color=color
              )
              await message.author.send(embed=embed)
            count_one+=1
            
          combined_variants = member.create_variant(
            material=channelData(chosen_variants, "material"),
            clothing_color=channelData(chosen_variants, "clothingcolor"),
            parts=channelData(chosen_variants, "parts"),
            progressive=channelData(chosen_variants, "progressive"),
            particle=channelData(chosen_variants, "particle"),
            emissive=channelData(chosen_variants, "emissive"),
            numeric=channelData(chosen_variants, "numeric"),
            pattern=channelData(chosen_variants, "pattern"),
            jersey_color=channelData(chosen_variants, "jerseycolor")
          )

          await member.set_outfit(
              asset=cosmetic.id,
              variants = combined_variants
          )     
          
          for v in chosen_variants:
            variantName = v['name']
            thumbnailVar = v['image']

            embed = discord.Embed(
              title=f"Variants Successfully Changed to {variantName}",
              description=member.outfit,
              color=color
            )
            
            try:
              embed.set_thumbnail(url=thumbnailVar)
            except:
              embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/fortnite_gamepedia/images/b/bb/Fortnite-T_Placeholder_Item_Outfit.png/revision/latest/scale-to-width-down/256?cb=20200722180525")
            embed.set_author(name="AtomicBot",icon_url=profileimg)
            embed.set_footer(text=footertext)
            await message.author.send(embed=embed)
              

        else:
          embed = discord.Embed(
                title="Error: You don't have a bot running!",
                description="Start a bot with **a!start**",
                color=color
              )
          await message.author.send(embed=embed)
        return


      
      if(args[0] == prefix + 'info'):
        embed = discord.Embed(
          title="**AtomicBot**",
          color=color
        )
        embed.add_field(
          name="**Commands**",
          value="Type " + prefix + "help for help",
          inline=False
        )
        embed.add_field(
          name="**Servers**",
          value=len(bot.guilds),
          inline=False
        )
        embed.add_field(
          name="**Bots Online**",
          value=len(botdict),
          inline=False
        )
        embed.add_field(
          name="**Coded By**",
          value="AtomicXYZ",
          inline=False
        )
        embed.add_field(
          name="**Website (With Invite Links)**",
          value=website,
          inline=False
        )
        embed.set_author(name="AtomicBot",icon_url=profileimg)
        embed.set_footer(text=footertext)
        await message.channel.send(embed=embed)
        return


      if(args[0] == prefix + 'ready'):
        member = client.party.me
        try:
          await member.set_ready(fortnitepy.ReadyState.READY)
          embed = discord.Embed(
            title="Bot set to Ready",
            description="Ready State: Ready",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Incorrect Command",
            description="Make sure the bot is not already in the ready state!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
      
      if(args[0] == prefix + 'match'):
        member = client.party.me
        try:
          if(args[1]):
            await member.set_in_match(players_left=int(args[1]))
            embed = discord.Embed(
              title="Bot set to In-Match Status with " + args[1] + " players remaining",
              color=color
            )
            embed.set_author(name="AtomicBot",icon_url=profileimg)
            embed.set_footer(text=footertext)
            await message.author.send(embed=embed)
          else:
            await member.set_in_match(players_left=100)
            embed = discord.Embed(
              title="Bot set to In-Match Status with 100 players remaining",
              color=color
            )
            embed.set_author(name="AtomicBot",icon_url=profileimg)
            embed.set_footer(text=footertext)
            await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Incorrect Command",
            description="Please provide a number or players remaining",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
      
      if(args[0] == prefix + 'unmatch'):
        member = client.party.me
        try:
          await member.clear_in_match()
          embed = discord.Embed(
            title="In-Match Status Cancelled",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Incorrect Command",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return

      # if(args[0] == prefix + 'clearemote'):
      #   member = client.party.me
      #   try:
      #     await member.clear_emote()
      #     embed = discord.Embed(
      #       title="Emote Cleared",
      #       color=color
      #     )
      #     embed.set_author(name="AtomicBot",icon_url=profileimg)
      #     embed.set_footer(text=footertext)
      #     await message.author.send(embed=embed)
      #     return
      #   except:
      #     embed = discord.Embed(
      #       title="Error",
      #       color=color
      #     )
      #     embed.set_author(name="AtomicBot",icon_url=profileimg)
      #     embed.set_footer(text=footertext)
      #     await message.author.send(embed=embed)
      #     return
      
      if(args[0] == prefix + 'sitout'):
        member = client.party.me
        try:

          await client.set_ready(fortnitepy.ReadyState.SITTING_OUT)

          embed = discord.Embed(
            title="Bot set to Sitting Out",
            description="Ready State: Sitting Out",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Incorrect Command",
            description="Make sure the bot is not already in the sitting out state!",
            color=color
          )
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return

      if(args[0] == prefix + 'unready' or args[0] == prefix + 'sitin'):
        member = client.party.me
        try:

          await member.set_ready(fortnitepy.ReadyState.NOT_READY)

          embed = discord.Embed(
              title="Bot set to Not Ready",
              description="Ready State: Not Ready",
              color=color
            )
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Incorrect Command",
            description="Make sure the bot is not already in the ready state!",
            color=color
          )
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return

      if(args[0] == prefix + 'privacy'):
        member = client.party
        try:
          if(member.leader):
            if(args[1].upper() == "PRIVATE"):
              await member.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
              embed = discord.Embed(
                title="Party Privacy Set to Private",
                description="Privacy: Private",
                color=color
              )
              embed.set_author(name="AtomicBot",icon_url=profileimg)
              embed.set_footer(text=footertext)
              await message.author.send(embed=embed)
              return
            elif(args[1].upper() == "PUBLIC"):
              await member.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
              embed = discord.Embed(
                title="Party Privacy Set to Public",
                description="Privacy: Public",
                color=color
              )
              embed.set_author(name="AtomicBot",icon_url=profileimg)
              embed.set_footer(text=footertext)
              await message.author.send(embed=embed)
              return
        except:
          embed = discord.Embed(
            title="Error: Incorrect Privacy",
            description="Make sure the bot is party leader and you typed **private or public**!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return

      if(args[0] == prefix + 'pinkghoul'):
        member = client.party.me
        command = "ghoul trooper"
        cosmetic = await fetch_cosmetic('AthenaCharacter', command)
        try:
          await member.set_outfit(
            asset=cosmetic.id,
            variants = member.create_variant(
              material=3
            )
          )
          embed = discord.Embed(
            title="Skin Successfully Changed to Pink Ghoul Trooper",
            description=cosmetic.id,
            color=color
          )
          embed.set_thumbnail(url=f"https://i.pinimg.com/originals/36/92/ee/3692eea092dce62732b7b65ab2f8cd1b.png")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Skin/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        
      if(args[0] == prefix + 'purpleskull'):
        member = client.party.me
        command = "skull trooper"
        cosmetic = await fetch_cosmetic('AthenaCharacter', command)
        try:
          await member.set_outfit(
            asset=cosmetic.id,
            variants = member.create_variant(
              clothing_color=1
            )
          )
          embed = discord.Embed(
            title="Skin Successfully Changed to Purple Skull Trooper",
            description=cosmetic.id,
            color=color
          )
          embed.set_thumbnail(url=f"https://i.redd.it/sgnjl7agwdl51.png")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Skin/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
      
      if(args[0] == prefix + 'emote'):
        cosmetic = await fetch_cosmetic('AthenaDance', command)
        member = client.party.me
        try:

          if(args[1] == 'none' or args[1] == 'clear'):
            await member.clear_emote()
            embed = discord.Embed(
              title="Emote Cleared",
              color=color
            )
            await message.author.send(embed=embed)
            return

          await member.set_emote(
            asset=cosmetic.id,
            run_for=emoteseconds
          )
          embed = discord.Embed(
          title="Emote Successfully Changed to " + cosmetic.name,
          description=cosmetic.id,
          color=color
          )
          try:
            embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{member.emote}/icon.png")
            # embed.set_thumbnail(url=f"https://benbot.app/cdn/images/{member.emote}/icon.png")
          except:
            embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/fortnite_gamepedia/images/b/bb/Fortnite-T_Placeholder_Item_Outfit.png/revision/latest/scale-to-width-down/256?cb=20200722180525")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
          
        except Exception as e:
          embed = discord.Embed(
            title="Error: Invalid Emote/ID",
            description=f"Error: {e}",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
      
      if(args[0] == prefix + 'eid'):
        member = client.party.me
        try:
          await member.set_emote(
            asset=args[1],
            run_for=emoteseconds
          )
          embed = discord.Embed(
          title="Emote Successfully Changed",
          description=member.emote,
          color=color
          )
          try:
            embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{member.emote}/icon.png")
            # embed.set_thumbnail(url=f"https://benbot.app/cdn/images/{member.emote}/icon.png")
          except:
            embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/fortnite_gamepedia/images/b/bb/Fortnite-T_Placeholder_Item_Outfit.png/revision/latest/scale-to-width-down/256?cb=20200722180525")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
          
        except:
          embed = discord.Embed(
            title="Error: Invalid Emote/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
      
      if(args[0] == prefix + 'backpack' or args[0] == prefix + 'backbling'):
        cosmetic = await fetch_cosmetic('AthenaBackpack', command)
        member = client.party.me
        try:
          
          if(args[1] == 'none' or args[1] == 'clear'):
            await member.clear_backpack()
            embed = discord.Embed(
              title="Backpack Cleared",
              color=color
            )
            await message.author.send(embed=embed)
            return
          
          await member.set_backpack(
            asset=cosmetic.id,
            variants = None
          )
          embed = discord.Embed(
            title="Backpack Successfully Changed to " + cosmetic.name,
            description=cosmetic.id,
            color=color
          )
          try:
            embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{member.backpack}/icon.png")
            # embed.set_thumbnail(url=f"https://benbot.app/cdn/images/{member.backpack}/icon.png")
          except:
            embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/fortnite_gamepedia/images/b/bb/Fortnite-T_Placeholder_Item_Outfit.png/revision/latest/scale-to-width-down/256?cb=20200722180525")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Backpack",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
      
      if(args[0] == prefix + 'bid'):
        member = client.party.me
        try:
          await member.set_backpack(
            asset=args[1],
            variants = None
          )
          embed = discord.Embed(
            title="Backpack Successfully Changed",
            description=member.backpack,
            color=color
          )
          try:
            embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{member.backpack}/icon.png")
            # embed.set_thumbnail(url=f"https://benbot.app/cdn/images/{member.backpack}/icon.png")
          except:
            embed.set_thumbnail(url=f"https://static.wikia.nocookie.net/fortnite_gamepedia/images/b/bb/Fortnite-T_Placeholder_Item_Outfit.png/revision/latest/scale-to-width-down/256?cb=20200722180525")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Backpack",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
      
      if(args[0] == prefix + 'level'):
        member = client.party.me
        banner_ico = member.banner[0]
        try:
          await member.set_banner(icon=banner_ico, season_level=int(command))
          embed = discord.Embed(
            title= "Level Successfully Changed to " + command,
            description = "Current Level: " + command,
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Level",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
    
      if(args[0] == prefix + 'say'):
        await client.party.send(command)
        embed = discord.Embed(
                title=
                "Successfully sent the message!",
                description=
                "Message: " + command,
                color=color)
        await message.author.send(embed=embed)

      if(args[0] == prefix + 'hide'):
        try:
          await set_and_update_party_prop(client,
                'Default:RawSquadAssignments_j', {
                    'RawSquadAssignments': [{'memberId': client.user.id, 'absoluteMemberIdx': 1}]
                }
            )
          embed = discord.Embed(
                title=
                "Successfully Hidden all Party Members!",
                description=
                "To unhide, type " + prefix + "unhide",
                color=color)
          await message.author.send(embed=embed)
        except:
          embed = discord.Embed(
                title=
                "Failed to Hide",
                description=
                "Make sure the bot is party leader!",
                color=color)
          await message.author.send(embed=embed)
        return
      
      if(args[0] == prefix + 'unhide'):
        try:
          for i in client.party.members:
            if(not client.user.display_name == i.display_name):
              await i.promote()
              break
          embed = discord.Embed(
                title=
                "Unhid all members!",
                description=
                "To hide again, promote the bot to party leader and type " + prefix + "hide",
                color=color)
          await message.author.send(embed=embed)
        except:
          embed = discord.Embed(
                title=
                "Failed to Unhide",
                description=
                "Make sure the bot is party leader!",
                color=color)
          await message.author.send(embed=embed)
        return

      if(args[0] == prefix + 'invite'):
        embeddone = discord.Embed(
          title=
          "Click here to invite AtomicBot to your own Discord Server!",
          url="https://discord.com/api/oauth2/authorize?client_id=829050201648922645&permissions=387136&scope=bot",
          color=color)
        await message.channel.send(embed=embeddone)
        return
    
    except Exception as e: 
      embed = discord.Embed(
          title = "Error",
          description = f"Please check for typos or report this bug to AtomicXYZ\n\nError: {e}",
          color=color
        )
      await message.channel.send(embed=embed)
      return
    await bot.process_commands(message)
    

@bot.command()
async def extract(ctx, path = None):
        try:
          if path is None:
                  await ctx.send('smh')
          
          elif "/Sounds/" in path:
                  epic = requests.get(f'https://api.gummyfn.com/export?path={path}')
                  with open("audio.ogg", "wb") as o:
                          o.write(epic.content)
                          o.close
                  await ctx.send(file=discord.File('audio.ogg'))
                  os.remove('audio.ogg')
          
          elif ".mp4" in path:
                  epic = requests.get(f'https://api.gummyfn.com/export?path={path}')
                  with open("video.mp4", "wb") as o:
                          o.write(epic.content)
                          o.close
                  await ctx.send(file=discord.File('video.mp4'))
                  os.remove('video.mp4')                
                  

          else:
                  epic = requests.get(f'https://api.gummyfn.com/export?path={path}')
                  with open("image.png", "wb") as o:
                          o.write(epic.content)
                          o.close
                  await ctx.send(file=discord.File('image.png'))
                  os.remove('image.png')
        except Exception as e:
          await ctx.send(e)

#TOKENS
      
# bot.run('ODMyMjYzNjcyODQzMDc1NjE0.YHhP8g.-XaEozpPh2QwZVQJSUkL0fsfS3I') # TEST TOKEN

bot.run(os.environ['DISCORD_TOKEN'])

# bot.run("ODI5MDUwMjAxNjQ4OTIyNjQ1.YGyfKw.Ll3lzer7STRx62O8bz1Dehvvxcw") # MAIN TOKEN
import os
import discord
import json
from discord.ext import commands
from fortnitepy.ext import commands as cmds
from typing import Optional, Union, Any
import crayons
import aiohttp
import BenBotAsync
import asyncio
import fortnitepy
from functools import partial


email = 'email@email.com'
password = 'password1'
filename = 'device_auths.json'




def getClient(authcode:str,premium:bool):
    acceptFriend = True
    acceptInvite = True
    status = 'AtomicBot by AtomicXYZ'
    banner = "brseason01"
    banner_color = "defaultcolor15"
    platform = 'PSN'
    joinMessage = ''

    try:
      client = fortnitepy.Client(auth=fortnitepy.AdvancedAuth(
        authorization_code=authcode),
        status=status,
        platform=fortnitepy.Platform(platform))

      def get_device_auth_details(self):
          if os.path.isfile(filename):
              with open(filename, 'r') as fp:
                  return json.load(fp)
          return

      def store_device_auth_details(self, email, details):
          existing = self.get_device_auth_details()
          existing[email] = details

          with open(filename, 'w') as fp:
              json.dump(existing, fp)

      async def event_device_auth_generate(self, details, email):
          self.store_device_auth_details(email, details)

      @client.event
      async def event_ready(self):
          print(crayons.blue(f"Client ready as  + {self.user.display_name}"))
          self.session = aiohttp.ClientSession()
          self.session_event.set()
          await edit_and_keep_client_member()
      
      async def edit_and_keep_client_member():
            member = client.party.me
            try:
              await member.edit_and_keep(
                partial(member.set_outfit, asset='CID_253_Athena_Commando_M_MilitaryFashion2'),
                partial(member.set_banner, icon="OtherBanner28", season_level=999),
                partial(member.set_emote, asset='EID_Floss',run_for=20)
              )
            except:
              print(crayons.red("Error Editing Styles"))
              return

    except:
      print(crayons.red("Invalid Auth Code"))
      return
    

    @client.event
    async def event_friend_request(request): 
      try:
        await request.accept()
      except:
        print(crayons.red("Friend Request Error"))

    @client.event
    async def event_party_invite(invitation):
      try:
        await invitation.accept()
        await edit_and_keep_client_member()
      except (fortnitepy.errors.HTTPException):
        print(crayons.red("Error Joining Party"))
        

    return client


loop = asyncio.get_event_loop()

prefix = 'a!'

color = 0xff0000
footertext = "AtomicBot v1.6 by AtomicXYZ"

intents = discord.Intents(messages=True, members=True)

bot = commands.Bot(command_prefix=prefix, intents=intents)

bot.remove_command('help')

async def fetch_cosmetic(type_, name):
    try:
      data = await BenBotAsync.get_cosmetic(
              lang="en",
              searchLang="en",
              matchMethod="full",
              name=name,
              backendType=type_
          )
    except:
      data = await BenBotAsync.get_cosmetic(
              lang="en",
              searchLang="en",
              matchMethod="contains",
              name=name,
              backendType=type_
          )
    return data

async def set_and_update_member_prop(self, schema_key: str, new_value: Any) -> None:
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.me.patch(updated=prop)

async def set_and_update_party_prop(self, schema_key: str, new_value: Any) -> None:
    prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

    await self.party.patch(updated=prop)

botlist = []
currentbots = {}
savedbots = {} # future idea of saving bots (cant be saved locally)

emoteseconds = 60
expiretime = 30
profileimg = "https://cdn.discordapp.com/avatars/829050201648922645/d8d62960d600af3975b61735ccc5e90c.png?size=128"

@bot.event
async def on_ready():
  print('Logged in')
  while True:
    await bot.change_presence(activity=discord.Game(name="made by AtomicXYZ"))
    await asyncio.sleep(10)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(len(bot.guilds)) + " Servers"))
    await asyncio.sleep(10)
    await bot.change_presence(activity=discord.Game(name="a!help"))
    await asyncio.sleep(10)
    await bot.change_presence(activity=discord.Game(name=f"{len(currentbots)} bots online"))
    await asyncio.sleep(10)
  
  


@bot.event
async def on_message(message):
    await asyncio.sleep(1)
    try:
      if message.channel.id == (831968067684007987):
          await message.delete()
    except:
      print('Error Deleting Message')
      return

    args = message.content.lower().split(' ')
    client = currentbots.get(message.author.id,None)
    split = args[1:]
    command = " ".join(split)
    skinurl = "-".join(split)
    if(args[0] == prefix + 'start'):
        global step
        await asyncio.sleep(1)
        try:
          await message.delete()
        except:
          pass

        if(client):
          embed=discord.Embed(
          title="Error: Bot Currently Running",
          description="The bot will now be closed", 
          color=color)
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          await client.close(close_http=True,dispatch_close=True)
          for i in step:
              i.cancel()
          botlist.remove(client)
          del currentbots[message.author.id]
          await client.wait_until_closed()
          embed=discord.Embed(
          title="Client Closed",
          description="Start a new bot with "+prefix+"start", 
          color=color)
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)

          return

        
        await asyncio.sleep(4)
        embed=discord.Embed(
        title="AtomicBot Control Panel",
        description="**Made by: AtomicXYZ**", 
        color=color)
        embed.set_author(name="AtomicBot",icon_url=profileimg)
        
        embed.add_field(
          name="**Step 1**", 
          value="Create an ALT Epic Games Account and sign into: https://epicgames.com", 
          inline=False)

        embed.add_field(
          name="**Step 2**", 
          value="[**Click Here**](https://www.epicgames.com/id/api/redirect?clientId=3446cd72694c4a4485d81b77adbb2141&responseType=code)", inline=False)
        
        embed.add_field(
          name="**Step 3**", 
          value="Paste the code from the website here\n(Refer to the image below for what to copy & paste)", inline=False)
        
        embed.set_image(url="https://media.discordapp.net/attachments/832266569815949352/836389927474298970/Screenshot-2021-04-26-195151.png")
        
        embed.add_field(
          name="**Type " + prefix + "cancel to cancel bot creation**", 
          value="(You can create a new bot later with " + prefix + "start)", 
          inline=False)

        embed.set_footer(text=footertext)

        await message.author.send(embed=embed)
        

        def check(msg):
          return (msg.content and (len(msg.content) == 32 or len(msg.content) == 8)) and msg.author.id == message.author.id

        msg = await bot.wait_for('message', check=check)

        if(msg.content.lower() == prefix + "cancel"):
          await asyncio.sleep(1)
          embeddone = discord.Embed(
            title=
            "Bot Creation Cancelled!",
            description=
            "Start a new Bot by typing " + prefix + "start",
            color=color)
          await message.author.send(embed=embeddone)
          return
        
        
        else:
          print("Bot Creation Started")
          
          client = getClient(msg.content,False)
        
        
        step = [
            bot.loop.create_task(client.start()),
            bot.loop.create_task(client.wait_until_ready())
        ]
        complete, _ = await asyncio.wait(step, return_when=asyncio.FIRST_COMPLETED)

        if(step[1] in complete):
          botlist.append(client)
          currentbots.update({message.author.id: client})
          print(crayons.green(f'Bot ready as {client.user.display_name}'))
          await client.wait_until_ready()
          await asyncio.sleep(1)
          embed = discord.Embed(
            title=f" Bot Control Panel for {client.user.display_name}",
            description= "**Type " + prefix + "help for the list of commands!**", 
            color=color)
          embed.set_thumbnail(url=f"https://cdn-0.skin-tracker.com/images/fnskins/icon/fortnite-summit-striker-outfit.png?ezimgfmt=rs:180x180/rscb10/ng:webp/ngcb10")
          embed.add_field(
            name="Friends", 
            value=f"{len(client.friends)}",
            inline=True)
          onlineFriends = []
          offlineFriends = []
          for i in client.friends:
            if(i.is_online()):
              onlineFriends.append(i)
            else:
              offlineFriends.append(i)
          embed.add_field(
            name="Online", 
            value=f"{len(onlineFriends)}",
            inline=True)
          embed.add_field(
            name="Offline", 
            value=f"{len(offlineFriends)}",
            inline=True)
          embed.add_field(
            name=f"Your Bot will expire in {expiretime} min", 
            value="\nType " + prefix + "stop to stop your bot",
            inline=False)
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)

          await message.author.send(embed=embed)

          await asyncio.sleep(expiretime*60)
          await client.close(close_http=True,dispatch_close=True)
          for i in step:
              i.cancel()
          botlist.remove(client)
          del currentbots[message.author.id]
          embeddone = discord.Embed(
            title=
            "Bot Time Expired!",
            description=
            "Restart Bot by typing " + prefix + "start",
            color=color)
          await message.author.send(embed=embeddone)
          return

        else:
          
          embed = discord.Embed(
            title="Bot was unable to start! (Most likely incorrect auth code)",
            description="You can create a new bot with " + prefix + "start",
            color=color)
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return

    try:
      if(args[0] == prefix + 'help'):
        if(client):
          embed = discord.Embed(
            title=f"Help Page for {client.user.display_name}",
            description="Commands must be sent in DMs",
            color=color
          )
          embed.add_field(
            name="**" + prefix + "stop**",
            value="Cancels your bot",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "skin**",
            value="Changes the bot's skin",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "emote**",
            value=f"Changes the bot's emote",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "backpack**",
            value="Changes the bot's backpack/backling",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "level**",
            value="Changes the bot's level",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "hide**",
            value="Hides all of the players in the party",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "unhide**",
            value="Unhides all of the players in the party",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "pinkghoul**",
            value="Equips the OG Pink Ghoul Trooper Skin",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "purpleskull**",
            value="Equips the OG Purple Skull Trooper Skin",
            inline = True
          )
          embed.add_field(
          name="**" + prefix + "variant**",
          value="Sets the variant of the current skin",
          inline = True
          )
          embed.add_field(
            name="**" + prefix + "ready**",
            value="Changes the bot's ready state to ready",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "unready**",
            value="Changes the bot's ready state to unready",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "say**",
            value="Sends a message from the bot in party chat",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "privacy**",
            value="Changes the bot's party privacy",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "sitout**",
            value="Makes the bot sit out",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "sitin**",
            value="Makes the bot sit in",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "invite**",
            value="Sends the bot's Discord Invite link",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "help**",
            value="Sends this message",
            inline = True
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          
          await message.author.send(embed=embed)
          return
        else:
          embed = discord.Embed(
            title=f"AtomicBot Help Page",
            description="Create a bot to see the full commands!",
            color=color
          )
          embed.set_thumbnail(url="https://media.discordapp.net/attachments/836446331992145950/836719691459461180/AtomicLogo.png")
          embed.add_field(
            name="**" + prefix + "start**",
            value="Creates a bot",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "stop**",
            value="Cancels your bot",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "invite**",
            value="Sends the bot's Discord Invite link",
            inline = True
          )
          embed.add_field(
            name="**" + prefix + "help**",
            value="sends this message",
            inline = True
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          
          await message.author.send(embed=embed)
          return
    
      if(args[0] == prefix + 'stop'):
        if(client.is_ready() or client in botlist or client in currentbots):
          await client.close(close_http=True,dispatch_close=True)
        for i in step:
          i.cancel()
        await client.wait_until_closed()
        print(crayons.red(f"Bot cancelled {client.user.display_name}"))
        botlist.remove(client)
        del currentbots[message.author.id]
        embeddone = discord.Embed(
          title=
          "Bot Cancelled!",
          description=
          "Restart Bot by typing " + prefix + "start",
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
          embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{member.outfit}/icon.png")
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
      
      if(args[0] == prefix + 'variant'):
        member = client.party.me
        try:
          if(args[1] == "material"):
            await member.set_outfit(
              asset=member.outfit,
              variants = member.create_variant(
                material = int(args[2])
              ) 
            )

          elif(args[1] == "clothing_color"):
            await member.set_outfit(
              asset=member.outfit,
              variants = member.create_variant(
                clothing_color = int(args[2])
              ) 
            )

          embed = discord.Embed(
            title="Variant Successfully Changed to " + cosmetic.name,
            description=member.outfit,
            color=color
          )
          embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{member.outfit}/icon.png")
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Variant",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
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
      
      if(args[0] == prefix + 'sitout'):
        member = client.party.me
        try:
          await member.set_ready(fortnitepy.ReadyState.SITTING_OUT)
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
          embed.set_author(name="AtomicBot",icon_url=profileimg)
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return

      if(args[0] == prefix + 'unready' or args[0] == prefix + "sitin"):
        member = client.party.me
        try:
          await member.set_ready(fortnitepy.ReadyState.NOT_READY)
          embed = discord.Embed(
              title="Bot set to Not Ready",
              description="Ready State: Not Ready",
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
            elif(args[1].upper() == "FRIENDS"):
              await memberset_privacy(fortnitepy.PartyPrivacy.FRIENDS)
              embed = discord.Embed(
                title="Party Privacy Set to Friends Only",
                description="Privacy: Friends",
                color=color
              )
              embed.set_author(name="AtomicBot",icon_url=profileimg)
              embed.set_footer(text=footertext)
              await message.author.send(embed=embed)
              return
        except:
          embed = discord.Embed(
            title="Error: Incorrect Privacy",
            description="Make sure the bot is party leader and you typed **private, public, or friends**!",
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
          embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{member.outfit}/icon.png")
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
          embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{member.outfit}/icon.png")
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
          if(args[1].lower() == "floss"):
            await member.set_emote(
              asset="EID_Floss",
              run_for=emoteseconds
            )
            embed = discord.Embed(
            title="Emote Successfully Changed to " + cosmetic.name,
            description="EID_Floss",
            color=color
            )
            embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{member.emote}/icon.png")
            embed.set_author(name="AtomicBot",icon_url=profileimg)
            embed.set_footer(text=footertext)
            await message.author.send(embed=embed)
            return
          else:
            await member.set_emote(
              asset=cosmetic.id,
              run_for=emoteseconds
            )
            embed = discord.Embed(
            title="Emote Successfully Changed to " + cosmetic.name,
            description=cosmetic.id,
            color=color
            )
            embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{member.emote}/icon.png")
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
      
      if(args[0] == prefix + 'backpack'):
        cosmetic = await fetch_cosmetic('AthenaBackpack', command)
        member = client.party.me
        try:
          await member.set_backpack(
            asset=cosmetic.id,
            variants = None
          )
          embed = discord.Embed(
            title="Backpack Successfully Changed to " + cosmetic.name,
            description=cosmetic.id,
            color=color
          )
          embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{member.backpack}/icon.png")
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
          await client.party.members[0].promote()
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
          description=
          "Use " + prefix + "start to get a bot!",
          color=color)
        await message.author.send(embed=embeddone)
        return

      if(args[0] == '!bots'):
        for i in botlist:
          print(i.user.display_name)
          embeddone = discord.Embed(
          title="Current Bots Running",
          description=i.user.display_name,
          color=color)
        await message.author.send(embed=embeddone)
        return

      if(args[0] == '!remove'):
        embeddone = discord.Embed(
        title="Removed Bot From List",
        description=botlist[int(args[1])],
        color=color)
        await message.author.send(embed=embeddone)
        botlist.remove(int(args[1]))
        return
    
    except: 
      embed = discord.Embed(
          title = "Error: Incorrect Command",
          description = "Make a bot by typing " + prefix + "start",
          color=color
        )
      await message.author.send(embed=embed)
      return
      
      

bot.run(os.environ['DISCORD_TOKEN'])
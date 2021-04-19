import os
import discord
import json
from discord.ext import commands
import crayons
import aiohttp
import BenBotAsync
import asyncio
import fortnitepy
from functools import partial


email = 'email@email.com'
password = 'password1'
filename = 'device_auths.json'


status = 'AtomicBot by AtomicXYZ'
banner = "brseason01"
banner_color = "defaultcolor15"
platform = 'PSN'
acceptFriend = True
acceptInvite = True
joinMessage = ''

def getClient(authcode:str):
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
          edit_and_keep_client_member()
      
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
      if(acceptFriend):   
        try:
          await request.accept()
        except:
          print(crayons.red("Friend Request Error"))
    
    @client.event
    async def event_party_invite(invitation):
      if(acceptInvite): 
        try:
          await invitation.accept()
        except:
          print(crayons.red("Error Joining Party"))
        await edit_and_keep_client_member()

    return client


loop = asyncio.get_event_loop()

prefix = 'a!'

color = 0xff0000
footertext = "AtomicBot v1.0 by AtomicXYZ"

intents = discord.Intents(messages=True, members=True)

bot = commands.Bot(command_prefix=prefix, intents=intents)

bot.remove_command('help')

async def fetch_cosmetic(type_, name):
    data = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="full",
            name=name,
            backendType=type_
        )
    return data

@bot.event
async def on_ready():
  print('Logged in')
  await bot.change_presence(activity=discord.Game(name="made by AtomicXYZ"))
  
botlist = []
currentbots = {}
savedbots = {}

emoteseconds = 60
expiretime = 30

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
        await asyncio.sleep(5)
        embed=discord.Embed(
        title="How to get an AtomicBot",
        description="**Made by: AtomicXYZ**", 
        color=color)
        embed.set_author(name="AtomicBot")
        
        embed.add_field(
          name="**Step 1**", 
          value="Create an ALT Epic Games Account and sign into: https://epicgames.com", 
          inline=False)

        embed.add_field(
          name="**Step 2**", 
          value="Go to: https://www.epicgames.com/id/api/redirect?clientId=3446cd72694c4a4485d81b77adbb2141&responseType=code", inline=False)
        
        embed.add_field(
          name="**Step 3**", 
          value="Paste the code here \n(Ex: 31b4363830c54832be2164cf1b935321)", inline=False)
        
        embed.add_field(
          name="Type " + prefix + "stop to cancel", 
          value="(You can create a new bot later with " + prefix + "start)", 
          inline=False)

        embed.set_footer(text=footertext)

        await message.author.send(embed=embed)

        def check(m):
          return m.content and len(m.content) == 32 and m.author.id == message.author.id

        msg = await bot.wait_for('message', check=check)

        print("Bot Creation Started")
        
        client = getClient(msg.content)
        
        
        
        global step
        step = [
            bot.loop.create_task(client.start()),
            bot.loop.create_task(client.wait_until_ready())
        ]
        complete, _ = await asyncio.wait(step, return_when=asyncio.FIRST_COMPLETED)

        if(step[1] in complete):
          botlist.append(client)
          currentbots.update({message.author.id: client})
          print(crayons.green(f'Bot ready as {client.user.display_name}'))
          embed = discord.Embed(
            title=f" Bot Control Panel for {client.user.display_name}",
            description= "**Type " + prefix + "help for the list of commands!**", 
            color=color)
          embed.set_thumbnail(url=f"https://cdn-0.skin-tracker.com/images/fnskins/icon/fortnite-summit-striker-outfit.png?ezimgfmt=rs:180x180/rscb10/ng:webp/ngcb10")
          embed.add_field(
            name="Friends", 
            value=f"{len(client.friends)}",
            inline=True)
          embed.add_field(
            name="Blocked Users", 
            value=f"{len(client.blocked_users)}",
            inline=True)
          embed.add_field(
            name=f"Your Bot will expire in {expiretime} min", 
            value="\nType " + prefix + "stop to stop your bot",
            inline=False)
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)

          await asyncio.sleep(expiretime*60)
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
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return

    try:
      if(args[0] == prefix + 'help'):
        embed = discord.Embed(
          title=f"Help Page for {client.user.display_name}",
          description="Commands must be sent in DMs",
          color=color
        )
        embed.set_thumbnail(url=f"https://cdn-0.skin-tracker.com/images/fnskins/icon/fortnite-summit-striker-outfit.png?ezimgfmt=rs:180x180/rscb10/ng:webp/ngcb10")
        embed.add_field(
          name=prefix + "stop",
          value="Cancels your bot",
          inline = True
        )
        embed.add_field(
          name=prefix + "skin",
          value="Changes the bot's skin",
          inline = True
        )
        embed.add_field(
          name=prefix + "emote",
          value=f"Changes the bot's emote\nThe emote will run for {emoteseconds} seconds",
          inline = True
        )
        embed.add_field(
          name=prefix + "backpack",
          value="Changes the bot's backpack/backling",
          inline = True
        )
        embed.add_field(
          name=prefix + "level",
          value="Changes the bot's level",
          inline = True
        )
        embed.add_field(
          name=prefix + "pinkghoul",
          value="Equips the OG Pink Ghoul Trooper Skin",
          inline = True
        )
        embed.add_field(
          name=prefix + "purpleskull",
          value="Equips the OG Purple Skull Trooper Skin",
          inline = True
        )
        embed.add_field(
        name=prefix + "variant",
        value="Sets the variant of the current skin",
        inline = True
        )
        embed.add_field(
          name=prefix + "ready",
          value="Changes the bot's ready state to ready",
          inline = True
        )
        embed.add_field(
          name=prefix + "unready",
          value="Changes the bot's ready state to unready",
          inline = True
        )
        embed.add_field(
          name=prefix + "privacy",
          value="Changes the bot's party privacy",
          inline = True
        )
        embed.set_author(name="AtomicBot")
        embed.set_footer(text=footertext)
        await message.author.send(embed=embed)
        return
    
      if(args[0] == prefix + 'stop'):
        for i in step:
          i.cancel()
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
            title="Skin Successfully Changed to " + command.upper(),
            description=cosmetic.id,
            color=color
          )
          embed.set_thumbnail(url=f"https://cdn-0.skin-tracker.com/images/fnskins/icon/fortnite-{skinurl}-outfit.png?ezimgfmt=rs:180x180/rscb10/ng:webp/ngcb10")
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Skin/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot")
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
            title="Variant Successfully Changed to " + command.upper(),
            description=member.outfit,
            color=color
          )
          embed.set_thumbnail(url=f"https://cdn-0.skin-tracker.com/images/fnskins/icon/fortnite-{skinurl}-outfit.png?ezimgfmt=rs:180x180/rscb10/ng:webp/ngcb10")
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Variant",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot")
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

      if(args[0] == prefix + 'unready'):
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
              embed.set_author(name="AtomicBot")
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
              embed.set_author(name="AtomicBot")
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
              embed.set_author(name="AtomicBot")
              embed.set_footer(text=footertext)
              await message.author.send(embed=embed)
              return
        except:
          embed = discord.Embed(
            title="Error: Incorrect Privacy",
            description="Make sure the bot is party leader and you typed **private, public, or friends**!",
            color=color
          )
          embed.set_author(name="AtomicBot")
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
            title="Skin Successfully Changed to PINK GHOUL TROOPER",
            description=cosmetic.id,
            color=color
          )
          embed.set_thumbnail(url=f"https://cdn-0.skin-tracker.com/images/fnskins/icon/fortnite-ghoul-trooper-outfit.png?ezimgfmt=rs:180x180/rscb10/ng:webp/ngcb10")
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Skin/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot")
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
            title="Skin Successfully Changed to PURPLE SKULL TROOPER",
            description=cosmetic.id,
            color=color
          )
          embed.set_thumbnail(url=f"https://cdn-0.skin-tracker.com/images/fnskins/icon/fortnite-skull-trooper-outfit.png?ezimgfmt=rs:180x180/rscb10/ng:webp/ngcb10")
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Skin/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot")
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
            title="Emote Successfully Changed to " + command.upper(),
            description="EID_Floss",
            color=color
            )
            embed.set_thumbnail(url=f"https://cdn-0.skin-tracker.com/images/fnskins/icon/fortnite-{skinurl}-emote.png?ezimgfmt=rs:180x180/rscb10/ng:webp/ngcb10")
            embed.set_author(name="AtomicBot")
            embed.set_footer(text=footertext)
            await message.author.send(embed=embed)
            return
          else:
            await member.set_emote(
              asset=cosmetic.id,
              run_for=emoteseconds
            )
            embed = discord.Embed(
            title="Emote Successfully Changed to " + command.upper(),
            description=cosmetic.id,
            color=color
            )
            embed.set_thumbnail(url=f"https://cdn-0.skin-tracker.com/images/fnskins/icon/fortnite-{skinurl}-emote.png?ezimgfmt=rs:180x180/rscb10/ng:webp/ngcb10")
            embed.set_author(name="AtomicBot")
            embed.set_footer(text=footertext)
            await message.author.send(embed=embed)
            return
          
        except:
          embed = discord.Embed(
            title="Error: Invalid Emote/ID",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot")
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
            title="Backpack Successfully Changed to " + command.upper(),
            description=cosmetic.id,
            color=color
          )
          embed.set_thumbnail(url=f"https://cdn-0.skin-tracker.com/images/fnskins/icon/fortnite-{skinurl}-back-bling.png?ezimgfmt=rs:180x180/rscb10/ng:webp/ngcb10")
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Backpack",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot")
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
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
          return
        except:
          embed = discord.Embed(
            title="Error: Invalid Level",
            description="Make sure you type the name correctly!",
            color=color
          )
          embed.set_author(name="AtomicBot")
          embed.set_footer(text=footertext)
          await message.author.send(embed=embed)
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

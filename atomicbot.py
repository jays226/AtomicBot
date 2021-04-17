import os
import discord
import sanic
from sanic.response import json
from sanic import Sanic
import requests
from discord.ext import commands
from discord.ext import tasks
from fn import getClient
import crayons
import aiohttp
import BenBotAsync
import asyncio
import fortnitepy

loop = asyncio.get_event_loop()
# app = sanic.Sanic("PirxcyPinger")

# @app.route('/')
# async def index(request):
# 	return json({'bot': 'online'})

prefix = 'a!'

color = 0xff0000
footertext = "AtomicBot v0.2 by AtomicXYZ"

intents = discord.Intents(messages=True, members=True)

bot = commands.Bot(command_prefix=prefix, intents=intents)

# url = f'https://{os.getenv("REPL_SLUG")}--{os.getenv("REPL_OWNER")}.repl.co'
# url2 = f'https://{os.getenv("REPL_SLUG")}.{os.getenv("REPL_OWNER")}.repl.co'
# requests.post('https://pinger.pirxcy.xyz/api/add', json={'url': url})
# requests.post('https://pinger.pirxcy.xyz/api/add', json={'url': url2})

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
  # await app.create_server(host="0.0.0.0",port=8000, return_asyncio_server=True)
  
botlist = []
currentbots = {}
savedbots = {}

emoteseconds = 60
expiretime = 20

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

  
bot.run('ODI5MDUwMjAxNjQ4OTIyNjQ1.YGyfKw.7nKU_gLRRJLFdGdoNVN0jKUk_NM')
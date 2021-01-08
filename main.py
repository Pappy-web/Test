import ctypes
import os
import json
import discord
from discord.ext import commands
import string
import random
import pyfiglet
import asyncio
import requests
from colorama import Fore, init
import time
from bs4 import BeautifulSoup as bs4
import aiohttp
from datetime import datetime
from itertools import cycle
import urllib
from urllib.parse import quote
from urllib.request import urlopen
from random import randint
init()
col = 0x773CBB
with open('config.json', 'r') as f:
    prefixes = json.load(f)
client = commands.Bot(command_prefix = prefixes["prefix"], case_insensitive = True, self_bot = True)

afkstr = prefixes["afk"]
prefixstr = prefixes["prefix"]
giveawaystr = prefixes["giveaway_sniper"]
client.remove_command('help')

global user

promote = 'Pluto - Self Bot '
afk_bool = False

@client.event
async def on_connect():
    print(Fore.LIGHTGREEN_EX + """\n______  _         _                     _____        _   __  ______         _   
| ___ \| |       | |                   /  ___|      | | / _| | ___ \       | |  
| |_/ /| | _   _ | |_   ___    ______  \ `--.   ___ | || |_  | |_/ /  ___  | |_ 
|  __/ | || | | || __| / _ \  |______|  `--. \ / _ \| ||  _| | ___ \ / _ \ | __|
| |    | || |_| || |_ | (_) |          /\__/ /|  __/| || |   | |_/ /| (_) || |_ 
\_|    |_| \__,_| \__| \___/           \____/  \___||_||_|   \____/  \___/  \__|\n\n""")
    print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Logged in: '+ Fore.LIGHTYELLOW_EX + f'{client.user.name}#{client.user.discriminator}' + Fore.RESET)
    print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Prefix: '+ Fore.LIGHTYELLOW_EX + f'{prefixstr}' + Fore.RESET)
    if giveawaystr == 1:
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Giveaway sniper: '+ Fore.LIGHTYELLOW_EX + f'On' + Fore.RESET)
    else:
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Giveaway sniper: '+ Fore.LIGHTYELLOW_EX + f'Off' + Fore.RESET)
    print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Afk message: '+ Fore.LIGHTYELLOW_EX + f'{afkstr}' + Fore.RESET)
    print("\n\n")

@client.event
async def on_message(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) and ctx.author != client.user and ctx.author.bot == False and afk_bool == True:
        with open('config.json', 'r') as f:
            afks = json.load(f)
        if afks["afk"] == '':
            afks["afk"] = "Hey. I am afk."
            with open('config.json', 'w') as f:
                json.dump(afks, f, indent = 4)
            await ctx.send(afks["afk"])
    with open('config.json', 'r') as f:
        d = json.load(f)
    if d["giveaway_sniper"] == True:
        if (('**giveaway**' in str(ctx.content).lower() or ('react with' in str(ctx.content).lower() and 'giveaway' in str(ctx.content).lower()))) and ctx.author.bot == True:
            try:
                await asyncio.sleep(5)
                await ctx.add_reaction("🎉")
                print(Fore.LIGHTBLUE_EX + "[/] " + Fore.LIGHTGREEN_EX + "Sniped giveaway from:" + Fore.LIGHTYELLOW_EX + " [" + ctx.guild.name + ", in channel: " + ctx.channel.name + "]" + Fore.RESET)
            except:
                print(
                    Fore.LIGHTBLUE_EX + '[/]  ' + Fore.LIGHTGREEN_EX + "Failed to snipe giveaway from:" + Fore.LIGHTYELLOW_EX + " [" + ctx.guild.name + ", in channel: " + ctx.channel.name + "]" + Fore.RESET)
        elif '<@' + str(client.user.id) + '>' in ctx.content and (
                'giveaway' in str(ctx.content).lower() or 'won' in ctx.content or 'winner' in str(ctx.content).lower()) and ctx.author.bot == True:        
            try:
                won = re.search("You won the \*\*(.*)\*\*", ctx.content).group(1)
            except:
                won = "UNKNOWN"
            print(
                Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + "You won a giveaway! : Giveaway Snipe from: " + Fore.LIGHTCYAN_EX + won + Fore.LIGHTYELLOW_EX + " [" + ctx.guild.name + ", in channel: " + ctx.channel.name + "]" + Fore.RESET)
    await client.process_commands(ctx)

@client.event
async def on_message_delete(message):
    with open('snipe.json', 'r') as f:
        d = json.load(f)    
    if message.author != client.user and message.author.bot == False and message.content != '':
        d[str(message.channel.id)] = {}
        d[str(message.channel.id)]["content"] = message.content
        d[str(message.channel.id)]["author"] = f'{message.author.name}#{message.author.discriminator}'
        d[str(message.channel.id)]["avatar"] = str(message.author.avatar_url)

    with open('snipe.json', 'w') as f:
        json.dump(d, f, indent = 4)

@client.event
async def on_message_edit(before, after):
    with open('editsnipe.json', 'r') as f:
        d = json.load(f)    
    if before.author != client.user and before.author.bot == False:
        d[str(before.channel.id)] = {}
        d[str(before.channel.id)]["content"] = before.content
        d[str(before.channel.id)]["author"] = f'{before.author.name}#{before.author.discriminator}'
        d[str(before.channel.id)]["avatar"] = str(before.author.avatar_url)

    with open('editsnipe.json', 'w') as f:
        json.dump(d, f, indent = 4)

@client.command()
async def snipe(ctx):
    await ctx.message.delete()
    with open('snipe.json', 'r') as f:
        d = json.load(f)
    if str(ctx.channel.id) not in d:
        embed = discord.Embed(description = '**There are no messages to snipe.**', colour = col)
        embed.set_footer(text = promote)
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(description = d[str(ctx.channel.id)]["content"], colour = col)
        embed.set_footer(text = promote)
        embed.set_author(name = d[str(ctx.channel.id)]["author"], icon_url = d[str(ctx.channel.id)]["avatar"])
        await ctx.send(embed = embed)

@client.command(aliases=['text2img', 'texttoimage', 'text2image'])
async def tti(ctx, *, txt):
    print("Due to this command,below here shows a error, but theres nothing to worry about.")
    api = f"http://api.img4me.com/?font=arial&fcolor=cc990c&size=24&type=png&text={txt}".format(quote(txt))	 
    html = urlopen(api).read()
    embed=discord.Embed(description="", colour=col)
    soup = bs4(html, features="html.parser")
    text = soup.get_text()
    embed.set_image(url=soup)
    await ctx.send(embed=embed)
      
@client.command()
async def editsnipe(ctx):
    await ctx.message.delete()
    with open('editsnipe.json', 'r') as f:
        d = json.load(f)
    if str(ctx.channel.id) not in d:
        embed = discord.Embed(description = '**There are no edited messages to snipe.**', color = col)
        embed.set_footer(text = promote)
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(description = d[str(ctx.channel.id)]["content"], colour = col)
        embed.set_footer(text = promote)
        embed.set_author(name = d[str(ctx.channel.id)]["author"], icon_url = d[str(ctx.channel.id)]["avatar"])
        await ctx.send(embed = embed)

@client.command()
async def prefix(ctx, *, newprefix=''):
    await ctx.message.delete()
    if newprefix == '':
        embed = discord.Embed(description = "**You have to specify a new prefix.**", colour = col)
        embed.set_footer(text = promote)
        return await ctx.send(embed = embed)
    client.command_prefix = str(newprefix)
    with open('config.json', 'r') as f:
        d = json.load(f)
    d["prefix"] = newprefix
    with open('config.json', 'w') as f:
        json.dump(d, f, indent = 4)
    embed = discord.Embed(description = f'**Successfully set your prefix to `{newprefix}`!**', colour = col) 
    embed.set_footer(text = promote)
    await ctx.send(embed = embed)
    prefixstr = prefixes["prefix"]
    os.system('cls')
    print(Fore.LIGHTGREEN_EX + """\n______  _         _                     _____        _   __  ______         _   
| ___ \| |       | |                   /  ___|      | | / _| | ___ \       | |  
| |_/ /| | _   _ | |_   ___    ______  \ `--.   ___ | || |_  | |_/ /  ___  | |_ 
|  __/ | || | | || __| / _ \  |______|  `--. \ / _ \| ||  _| | ___ \ / _ \ | __|
| |    | || |_| || |_ | (_) |          /\__/ /|  __/| || |   | |_/ /| (_) || |_ 
\_|    |_| \__,_| \__| \___/           \____/  \___||_||_|   \____/  \___/  \__|\n\n""")
    print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Logged in: '+ Fore.LIGHTYELLOW_EX + f'{client.user.name}#{client.user.discriminator}' + Fore.RESET)
    print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Prefix: '+ Fore.LIGHTYELLOW_EX + f'{newprefix}' + Fore.RESET)
    if giveawaystr == 1:
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Giveaway sniper: '+ Fore.LIGHTYELLOW_EX + f'On' + Fore.RESET)
    else:
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Giveaway sniper: '+ Fore.LIGHTYELLOW_EX + f'Off' + Fore.RESET)
    print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Afk message: '+ Fore.LIGHTYELLOW_EX + f'{afkstr}' + Fore.RESET)
    print("\n\n")
    
@client.command()
async def terminal(ctx):
    await ctx.message.delete()
    os.system('cls')
    
@client.command()
async def emojitext(ctx, *, txt):
    await ctx.message.delete()
    tosend = ''
    l = len(txt)
    for i in range(0, l):
        ch = txt[i].lower()
        if ch >= '0' and ch <= '9':
            if ch == '0':
                tosend += ':zero: '
            if ch == '1':
                tosend += ':one: '
            if ch == '2':
                tosend += ':two: '
            if ch == '3':
                tosend += ':three: '
            if ch == '4':
                tosend += ':four: '
            if ch == '5':
                tosend += ':five: '
            if ch == '6':
                tosend += ':six: '
            if ch == '7':
                tosend += ':seven: '
            if ch == '8':
                tosend += ':zero: '
            if ch == '9':
                tosend += ':zero: '  
        else:
            if ch >= 'a' and ch <= 'z':
                tosend += ':regional_indicator_' + ch + ': '
            elif ch == ' ':
                tosend += '     '

            else:
                tosend += txt[i]

    if len(tosend) > 2000:
        await ctx.send('Your text exceeded the 2000 character limit.')
    else:
        await ctx.send(tosend)  

@client.command()
async def afk(ctx, *, message=''):
    global afk_bool
    await ctx.message.delete()
    if message != '':
        with open('config.json', 'r') as f:
            d = json.load(f)
        d["afk"] = message
        with open('config.json', 'w') as f:
            json.dump(d, f, indent = 4)
        embed = discord.Embed(description = f'**Successfully set your afk message to:`{message}`.**', colour = col)
        embed.set_footer(text=promote)
        await ctx.send(embed = embed)
        os.system('cls')
        print(Fore.LIGHTGREEN_EX + """\n______  _         _                     _____        _   __  ______         _   
| ___ \| |       | |                   /  ___|      | | / _| | ___ \       | |  
| |_/ /| | _   _ | |_   ___    ______  \ `--.   ___ | || |_  | |_/ /  ___  | |_ 
|  __/ | || | | || __| / _ \  |______|  `--. \ / _ \| ||  _| | ___ \ / _ \ | __|
| |    | || |_| || |_ | (_) |          /\__/ /|  __/| || |   | |_/ /| (_) || |_ 
\_|    |_| \__,_| \__| \___/           \____/  \___||_||_|   \____/  \___/  \__|\n\n""")
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Logged in: '+ Fore.LIGHTYELLOW_EX + f'{client.user.name}#{client.user.discriminator}' + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Prefix: '+ Fore.LIGHTYELLOW_EX + f'{prefixstr}' + Fore.RESET)
        if giveawaystr == 1:
            print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Giveaway sniper: '+ Fore.LIGHTYELLOW_EX + f'On' + Fore.RESET)
        else:
            print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Giveaway sniper: '+ Fore.LIGHTYELLOW_EX + f'Off' + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Afk message: '+ Fore.LIGHTYELLOW_EX + f'{message}' + Fore.RESET)
        print("\n\n")
    if afk_bool == True and message == '':
        afk_bool = False
        embed = discord.Embed(description = '**Successfully disabled afk.**', colour = col)
        embed.set_footer(text=promote)
        await ctx.send(embed = embed)

    elif afk_bool == False:
        afk_bool = True
        embed = discord.Embed(description = '**Successfully enabled afk.**', colour = col)
        embed.set_footer(text=promote)
        await ctx.send(embed = embed)

@client.command()
async def playing(ctx, *, game=''):
    await ctx.message.delete()
    if game == '':
        embed = discord.Embed(description = f'**You have to specify the game name.**', colour = col)
        embed.set_footer(text=promote)
        return await ctx.send(embed = embed)
    await client.change_presence(activity=discord.Game(name=game))
    embed = discord.Embed(description = f'**Successfully set your status to `playing {game}`.**', colour = col)
    embed.set_footer(text=promote)
    await ctx.send(embed = embed)

@client.command()
async def watching(ctx, *, watch=''):
    await ctx.message.delete()
    if watch == '':
        embed = discord.Embed(description = f'**You have to specify what you are watching.**', colour = col)
        embed.set_footer(text=promote)
        return await ctx.send(embed = embed)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=watch))
    embed = discord.Embed(description = f'**Successfully set your status to `watching {watch}`.**', colour = col)
    embed.set_footer(text=promote)
    await ctx.send(embed = embed)

@client.command()
async def streaming(ctx, *, stream=''):
    await ctx.message.delete()
    if stream == '':
        embed = discord.Embed(description = f'**You have to specify what you are streaming.**', colour = col)
        embed.set_footer(text=promote)
        return await ctx.send(embed = embed)
    await client.change_presence(activity=discord.Streaming(name=stream, url='https://www.twitch.tv/twitch'))
    embed = discord.Embed(description = f'**Successfully set your status to `streaming {stream}`.**', colour = col)
    embed.set_footer(text=promote)
    await ctx.send(embed = embed)

@client.command()
async def listening(ctx, *, listen=''):
    await ctx.message.delete()
    if listen == '':
        embed = discord.Embed(description = f'**You have to specify what you are listening to.**', colour = col)
        embed.set_footer(text=promote)
        return await ctx.send(embed = embed)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=listen))
    embed = discord.Embed(description = f'**Successfully set your status to `listening to {listen}`.**', colour = col)
    embed.set_footer(text=promote)
    await ctx.send(embed = embed)

@client.command()
async def embed(ctx, *, message):
    await ctx.message.delete()
    embed = discord.Embed(description = message, colour = col)
    embed.set_footer(text = promote)
    await ctx.send(embed = embed)

@client.command()
async def nitro(ctx):
    await ctx.message.delete()
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    await ctx.send(f'https://discord.gift/{code}')

@client.command()
async def purge(ctx, count, user: discord.User=None):
    await ctx.message.delete()
    user = ctx.author if not user else user
    try:
        count = int(count)
    except:
        await ctx.send('The amount has to be a number')
        return
    if count <= 0:
        await ctx.send('The amount has to be 1 or more.')
        return
    e = 0
    async for message in ctx.message.channel.history():
        if message.author == user:
            if e == count:
                return
            e += 1
            try:
                await message.delete()
            except discord.Forbidden:
                return

@client.command(aliases=["fancy"])
async def ascii(ctx, *, text):
    await ctx.message.delete()
    r = requests.get(f'http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}').text
    if len('```' + r + '```') > 2000:
        await ctx.send('The text is too long. (Max 2000 characters)')
        return
    await ctx.send(f"```{r}```")

@client.command()
async def spam(ctx, amount, *, text):
    await ctx.message.delete()
    try:
        amount = int(amount)
    except:
        await ctx.send('**The amount is invalid.**')
        return
    if amount <= 0:
        await ctx.send('**The amount has to be 1 or more.**')
        return
    for e in range(amount):
        await ctx.send(text)

@client.command(aliases=['wouldyourather', 'would-you-rather', 'wyrq'])
async def wyr(ctx): 
    await ctx.message.delete()
    r = requests.get('https://www.conversationstarters.com/wyrqlist.php').text
    soup = bs4(r, 'html.parser')
    qa = soup.find(id='qa').text
    qb = soup.find(id='qb').text
    embed = discord.Embed(title = 'Would You Rather?', description = f'```🅰 = {qa}```\n\n**OR**\n\n```🅱 = {qb}```', colour = col)
    embed.set_footer(text=promote)
    message = await ctx.send(embed = embed)
    await message.add_reaction("🅰")
    await message.add_reaction("🅱")

@client.command()
async def minesweeper(ctx, size: int = 5):
    await ctx.message.delete()
    size = max(min(size, 8), 2)
    bombs = [[random.randint(0, size - 1), random.randint(0, size - 1)] for x in range(int(size - 1))]
    is_on_board = lambda x, y: 0 <= x < size and 0 <= y < size
    has_bomb = lambda x, y: [i for i in bombs if i[0] == x and i[1] == y]
    m_offets = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]
    m_numbers = [
    ":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
    ":six:"
]
    message = "**Click to play**:\n"
    for y in range(size):
        for x in range(size):
            tile = "||{}||".format(chr(11036))
            if has_bomb(x, y):
                tile = "||{}||".format(chr(128163))
            else:
                count = 0
                for xmod, ymod in m_offets:
                    if is_on_board(x + xmod, y + ymod) and has_bomb(x + xmod, y + ymod):
                        count += 1
                if count != 0:
                    tile = "||{}||".format(m_numbers[count - 1])
            message += tile
        message += "\n"
    embed = discord.Embed(title = 'Minesweeper', description = message, colour = col)
    embed.set_footer(text=promote)
    await ctx.send(embed=embed)


@client.command(aliases=['geolocate', 'iptogeo', 'iptolocation', 'ip2geo', 'geoip'])
async def ip(ctx, *, ipaddr: str = ''):
    await ctx.message.delete()
    if ipaddr == '':
        col = random.randint(0, 0xffffff)
        embed = discord.Embed(description = f'**You need to specify an ip address.**\n\n`You can do {prefixstr}ip me to check your own ip.', colour = col)
        embed.set_footer(text=copyright)
        await ctx.send(embed=embed)
        return
    if ipaddr.lower() == 'me':
        r = requests.get(f'http://extreme-ip-lookup.com/json/')
    else:
        r = requests.get(f'http://extreme-ip-lookup.com/json/{ipaddr}')
    geo = r.json()
    embed = discord.Embed(color=col)
    fields = [
        {'name': 'IP', 'value': geo['query']},
        {'name': 'Type', 'value': geo['ipType']},
        {'name': 'Country', 'value': geo['country']},
        {'name': 'City', 'value': geo['city']},
        {'name': 'Continent', 'value': geo['continent']},
        {'name': 'Country', 'value': geo['country']},
        {'name': 'Hostname', 'value': geo['ipName']},
        {'name': 'ISP', 'value': geo['isp']},
        {'name': 'Latitute', 'value': geo['lat']},
        {'name': 'Longitude', 'value': geo['lon']},
        {'name': 'Org', 'value': geo['org']},
        {'name': 'Region', 'value': geo['region']},
    ]
    embed.set_footer(text=promote)
    for field in fields:
        if field['value']:
            embed.add_field(name=field['name'], value=field['value'], inline=True)
    return await ctx.send(embed=embed)

@client.command(pass_context = True, aliases = ['giveaway_sniper', 'giveawaysniper'])
async def giveaway(ctx, param):
    await ctx.message.delete()
    if param.lower() in ['yes', 'on', '1', 'true']:
        mode = 1 
    elif param.lower() in ['no', 'off', '0', 'false']:
        mode = 0
    else:
        await ctx.send('**That is not a valid option!**\n`Try `on` to turn the sniper on.\nTry `off` to turn the sniper off.')
        return
    with open('config.json', 'r') as f:
        d = json.load(f)
    d["giveaway_sniper"] = mode
    with open('config.json', 'w') as f:
        json.dump(d, f, indent = 4)
    if mode == 1:
        description = '**Successfully enabled the giveaway sniper.**'
        os.system('cls')
        print(Fore.LIGHTGREEN_EX + """\n______  _         _                     _____        _   __  ______         _   
| ___ \| |       | |                   /  ___|      | | / _| | ___ \       | |  
| |_/ /| | _   _ | |_   ___    ______  \ `--.   ___ | || |_  | |_/ /  ___  | |_ 
|  __/ | || | | || __| / _ \  |______|  `--. \ / _ \| ||  _| | ___ \ / _ \ | __|
| |    | || |_| || |_ | (_) |          /\__/ /|  __/| || |   | |_/ /| (_) || |_ 
\_|    |_| \__,_| \__| \___/           \____/  \___||_||_|   \____/  \___/  \__|\n\n""")
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Logged in: '+ Fore.LIGHTYELLOW_EX + f'{client.user.name}#{client.user.discriminator}' + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Prefix: '+ Fore.LIGHTYELLOW_EX + f'{prefixstr}' + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Giveaway sniper: '+ Fore.LIGHTYELLOW_EX + f'On' + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Afk message: '+ Fore.LIGHTYELLOW_EX + f'{afkstr}' + Fore.RESET)
        print("\n\n")    
    else:
        description = '**Successfully disabled the giveaway sniper.**'
        os.system('cls')
        print(Fore.LIGHTGREEN_EX + """\n______  _         _                     _____        _   __  ______         _   
| ___ \| |       | |                   /  ___|      | | / _| | ___ \       | |  
| |_/ /| | _   _ | |_   ___    ______  \ `--.   ___ | || |_  | |_/ /  ___  | |_ 
|  __/ | || | | || __| / _ \  |______|  `--. \ / _ \| ||  _| | ___ \ / _ \ | __|
| |    | || |_| || |_ | (_) |          /\__/ /|  __/| || |   | |_/ /| (_) || |_ 
\_|    |_| \__,_| \__| \___/           \____/  \___||_||_|   \____/  \___/  \__|\n\n""")
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Logged in: '+ Fore.LIGHTYELLOW_EX + f'{client.user.name}#{client.user.discriminator}' + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Prefix: '+ Fore.LIGHTYELLOW_EX + f'{prefixstr}' + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Giveaway sniper: '+ Fore.LIGHTYELLOW_EX + f'Off' + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Afk message: '+ Fore.LIGHTYELLOW_EX + f'{afkstr}' + Fore.RESET)
        print("\n\n")    
    embed = discord.Embed(description = description, color = col)
    embed.set_footer(text = promote)
    await ctx.send(embed = embed)

@client.command(aliases = ['enlargeemoji'])
async def bigemoji(ctx, emoji: discord.Emoji = None):
    await ctx.message.delete()
    if emoji == None:
        await ctx.send("**You have to specify an emoji to enlarge.**")
        return
    await ctx.send(emoji.url)

@client.command()
async def poll(ctx, *, message=''):
        await ctx.message.delete()
        if message == '':
            await ctx.send('**Please specify a question or topic.**')
        else:
            embed = discord.Embed(
                description = message,
                colour = col,
            )
            embed.set_thumbnail(url='https://img2.pngio.com/download-free-png-poll-png-6-png-image-dlpngcom-poll-png-800_800.jpg')
            embed.set_footer(text='👍 - YES 👎 - NO')
            sent = await ctx.send(embed=embed)
            await sent.add_reaction('👍')
            await sent.add_reaction('👎')

@client.command()
async def firstmessage(ctx):
    await ctx.message.delete()
    first_message = (await ctx.channel.history(limit=1, oldest_first=True).flatten())[0]
    embed = discord.Embed(description=first_message.content, color = col)
    embed.add_field(name="First Message", value=f"[Jump]({first_message.jump_url})")
    embed.set_author(name = f'{first_message.author.name}#{first_message.author.discriminator}', icon_url = first_message.author.avatar_url)
    embed.set_footer(text=promote)
    await ctx.send(embed=embed)

@client.command()
async def magik(ctx, user: discord.User = None):
    await ctx.message.delete()
    endpoint = "https://nekobot.xyz/api/imagegen?type=magik&intensity=3&image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"{user.name}_magik.png"))
        except:
            await ctx.send(res['message'])
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"{user.name}_magik.png"))
        except:
            await ctx.send(res['message'])

@client.command()
async def fry(ctx, user: discord.User = None):
    await ctx.message.delete()
    endpoint = "https://nekobot.xyz/api/imagegen?type=deepfry&image="
    if user is None:
        avatar = str(ctx.author.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"{user.name}_fry.png"))
        except:
            await ctx.send(res['message'])
    else:
        avatar = str(user.avatar_url_as(format="png"))
        endpoint += avatar
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(str(res['message'])) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"{user.name}_fry.png"))
        except:
            await ctx.send(res['message'])

@client.command()
async def tweet(ctx, username: str = None, *, message: str = None):
    await ctx.message.delete()
    if username is None or message is None:
        await ctx.send(f"**Incorrect format.**\nPlease use:\n`{prefixstr}tweet [username] [message]`")
        return
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}") as r:
            res = await r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"rain_tweet.png"))
            except:
                await ctx.send(res['message'])

@client.command(name="8ball")
async def _8ball(ctx, *, question=''):
        await ctx.message.delete()
        if question == '':
            print('**Please specify a question to ask 8ball.**')
        
        else:
            answer = [
                'As I see it, yes.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                'Don’t count on it.',
                'It is certain.',
                'It is decidedly so.',
                'Most likely.',
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Outlook good.',
                'Reply hazy, try again.',
                'Signs point to yes.',
                'Very doubtful.',
                'Without a doubt.',
                'Yes.',
                'Yes – definitely.',
                'You may rely on it.'
            ]
            answers = random.choice(answer)
            embed = discord.Embed(
                title = '8ball',
                description = 'Question: **' + question + '**\n\nAnswer: **' + answers + '**',
                colour = col
            )
            embed.set_footer(text = promote)
            embed.set_thumbnail(url = 'https://i.imgur.com/QeTgMAi.png')
            await ctx.send(embed = embed)

@client.command(aliases=["calc", "math"])
async def calculate(ctx, *, operation=None):
    await ctx.message.delete()
    try:
        operation = eval(operation)
    except ZeroDivisionError:
        await ctx.send(f"**Error: division by zero!**")
        return
    except:
        await ctx.send(f"**Error: expression could not be calculated!**")
        return
    await ctx.send(f"**The answer to your calculation is: **`{operation}`**!**")

@client.command(aliases=['slots', "slotmachine"])
async def slot(ctx):
    await ctx.message.delete()
    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
    a = random.choice(emojis)
    b = random.choice(emojis)
    c = random.choice(emojis)
    slotmachine = f"**{a} | {b} | {c}\n\n**"
    if a == b == c:
        embed=discord.Embed(title="Slot machine", description= f"{slotmachine} **3 in a row, you won!**", colour=col)
        embed.set_footer(text=promote)
        await ctx.send(embed=embed)
    elif (a == b) or (a == c) or (b == c):
            embed=discord.Embed(title="Slot machine", description=f"{slotmachine} **2 in a row, you won!**", colour=col)
            embed.set_footer(text=promote)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Slot machine", description= f"{slotmachine} **No match, you lost**", colour=col)
        embed.set_footer(text=promote)
        await ctx.send(embed=embed)

@client.command(aliases=['flip', 'coin'])
async def coinflip(self, ctx):
    coinsides = ['Heads', 'Tails']
    embed = discord.Embed(description=f"Your coin landed on {random.choice(coinsides)}", colour=col)
    embed.set_thumbnail(url="https://bootstraplogos.com/wp-content/uploads/edd/2018/10/logo-4.png")
    embed.set_footer(text=promote)
    await ctx.send(embed=embed)
        
@client.command(aliases = ["gayrate"])
async def howgay(ctx, *, name=''):
    await ctx.message.delete()
    col = random.randint(0, 0xffffff)
    embed = discord.Embed(
        title = 'Gay Rate Machine',
        description = ':rainbow_flag: Calculating...',
        color = col
    )
    embed.set_footer(text = promote)
    sent = await ctx.send(embed = embed)

    await asyncio.sleep(2)
    
    number = random.randrange(0, 101)
    desc = ''
    if name == '':
        desc = f'You are {number}% gay :rainbow_flag:'   
    else:
        desc = f'{name} is {number}% gay :rainbow_flag:'       
    embed1 = discord.Embed(
        title = 'Gay Rate Machine',description = desc, color = col)
    embed1.set_footer(text = promote)
    await sent.edit(embed = embed1)

@client.command(aliases = ["simprate:"])
async def howsimp(ctx, *, name=''):
    await ctx.message.delete()
    col = random.randint(0, 0xffffff)
    embed = discord.Embed(
        title = 'Simp Rate Machine',
        description = ':pleading_face: Calculating...',
        color = col
    )
    embed.set_footer(text = promote)
    sent = await ctx.send(embed = embed)

    await asyncio.sleep(2)
    
    number = random.randrange(0, 101)
    desc = ''
    if name == '':
        desc = f'You are {number}% simp :pleading_face:'   
    else:
        desc = f'{name} is {number}% simp :pleading_face:'       
    embed1 = discord.Embed(
        title = 'Simp Rate Machine',description = desc, color = col)
    embed1.set_footer(text = promote)
    
    await sent.edit(embed = embed1)

@client.command()
async def pp(ctx, *, name=''):

    await ctx.message.delete()
    col = random.randint(0, 0xffffff)
    embed = discord.Embed(
        title = 'Pp Machine',description = 'Calculating... :eggplant:',color = col)
    embed.set_footer(text = promote)
    sent = await ctx.send(embed = embed)

    await asyncio.sleep(2)
    
    number = random.randrange(0, 20)
    size = '=' * number
    desc = ''
    if name == '':
        desc = f"Your pp :eggplant:\n8{size}D"   
    else:
        desc = f" {name}'s pp :eggplant:\n8{size}D"          
    embed1 = discord.Embed(
        title = 'peepee machine', description = desc, color = col)
    embed1.set_footer(text = promote)
    
    await sent.edit(embed = embed1)

@client.command(aliases=['bitcoin'])
async def btc(ctx):
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,GBP')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    em = discord.Embed(description=f'USD: ${str(usd)}\nEUR: €{str(eur)}\nGBP: £{str(gbp)}', colour=col)
    em.set_author(name='BITCOIN', icon_url='https://cdn.pixabay.com/photo/2013/12/08/12/12/bitcoin-225079_960_720.png')
    await ctx.send(embed=em)
        
@client.command(aliases=['ethereum'])
async def eth(ctx):
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR,GBP')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    em = discord.Embed(description=f'USD: ${str(usd)}\nEUR: €{str(eur)}\nGBP: £{str(gbp)}', colour=col)
    em.set_author(name='ETHEREUM', icon_url='https://cdn.discordapp.com/attachments/271256875205525504/374282740218200064/2000px-Ethereum_logo.png')
    await ctx.send(embed=em)
    
@client.command()
async def xrp(ctx):
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=XRP&tsyms=USD,EUR,GBP')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    em = discord.Embed(description=f'USD: ${str(usd)}\nEUR: €{str(eur)}\nGBP: £{str(gbp)}', colour=col)
    em.set_author(name='XRP', icon_url='https://s2.coinmarketcap.com/static/img/coins/32x32/52.png')
    await ctx.send(embed=em)

@client.command(aliases=['tether'])
async def usdt(ctx):
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=USDT&tsyms=USD,EUR,GBP')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    em = discord.Embed(description=f'USD: ${str(usd)}\nEUR: €{str(eur)}\nGBP: £{str(gbp)}', colour=col)
    em.set_author(name='TETHER', icon_url='https://assets.coingecko.com/coins/images/325/large/Tether-logo.png?1598003707')
    await ctx.send(embed=em)

@client.command(aliases=['bitcoincash'])
async def bch(ctx):
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BCH&tsyms=USD,EUR,GBP')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    em = discord.Embed(description=f'USD: ${str(usd)}\nEUR: €{str(eur)}\nGBP: £{str(gbp)}', colour=col)
    em.set_author(name='BITCOIN CASH', icon_url='https://s2.coinmarketcap.com/static/img/coins/32x32/1831.png')
    await ctx.send(embed=em)
        
@client.command(aliases=['litecoin'])
async def ltc(ctx):
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD,EUR,GBP')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    gbp = r['GBP']
    em = discord.Embed(description=f'USD: ${str(usd)}\nEUR: €{str(eur)}\nGBP: £{str(gbp)}', colour=col)
    em.set_author(name='LITECOIN', icon_url='https://s2.coinmarketcap.com/static/img/coins/32x32/2.png')
    await ctx.send(embed=em)

@client.command()
async def junk(ctx):
    await ctx.message.delete()
    e = '‎‎‏‏‎‏‏‎ ‎‎\n'
    text = 166*e
    await ctx.send(text)

@client.command(aliases=['namecolor', 'namecolour'])
async def rainbowrole(ctx, *, role: discord.Role):
    await ctx.message.delete()
    embed = discord.Embed(description = f'**Started changing the color for {role.mention}.**', color = col)
    embed.set_footer(text=promote)
    await ctx.send(embed = embed)
    count = True
    while count == True:
        try:
            await role.edit(role=role, colour=0xFF0000)
            await asyncio.sleep(0.1)
            await role.edit(role=role, colour=0xFF7F00)
            await asyncio.sleep(0.1)
            await role.edit(role=role, colour=0xFFFF00)
            await asyncio.sleep(0.1)
            await role.edit(role=role, colour=0x00FF00)
            await asyncio.sleep(0.1)
            await role.edit(role=role, colour=0x0000FF)
            await asyncio.sleep(0.1)
            await role.edit(role=role, colour=0x4B0082)
            await asyncio.sleep(0.1)
            await role.edit(role=role, colour=0x9400D3)
            await asyncio.sleep(0.1)
        except:
            count = False

@rainbowrole.error
async def rainbow_error(ctx, error):
    await ctx.message.delete()
    if isinstance(error, commands.RoleNotFound):
        await ctx.send("**Role not found.**")

@client.command()
async def hypesquad(ctx, house):
    await ctx.message.delete()
    with open('config.json', 'r') as f:
        d = json.load(f)
    request = requests.Session()
    headers = {
        'Authorization': d["token"],
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
    }
    if house.lower() == "bravery":
        payload = {'house_id': 1}
    elif house.lower() == "brilliance":
        payload = {'house_id': 2}
    elif house.lower() == "balance":
        payload = {'house_id': 3}
    elif house.lower() == "random":
        houses = [1, 2, 3]
        payload = {'house_id': random.choice(houses)}
    else:
        await ctx.send("Invalid format.\nPlease use: {prefixstr}`hypesquad bravery / brilliance / balance / random`")
        return
    try:
        request.post('https://discordapp.com/api/v6/hypesquad/online', headers=headers, json=payload, timeout=10)
        embed = discord.Embed(description = f"**Your hypesquad badge is {house}.**", color = col)
        await ctx.send(embed=embed)
    except Exception as e:
        print(f"{Fore.RED}[/] Error: {e}" + Fore.RESET)

@client.command()
async def raid(ctx):
    await ctx.message.delete()
    if str(ctx.channel.type) != 'text':
            await ctx.send('You can not use this command here.')
            return
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
        except:
            pass
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
        except:
            pass
    try:
        await ctx.guild.edit(
            name=RandString(),
            description="Pluto - Self Bot",
            reason="Pluto - Self Bot",
            icon=None,
            banner=None
        )
    except:
        pass
    for i in range(250):
        try:
            await ctx.guild.create_text_channel(name="Pluto - Self Bot")
        except:
            pass
        await ctx.guild.create_role(name="Pluto - Self Bot", color=col)

@client.command()  
async def feed(ctx):
    r = requests.get("https://nekos.life/api/v2/img/feed")
    res = r.json()
    em = discord.Embed(description=f"<@{ctx.author.id}> feeds you.", colour=col)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)
    
@client.command()  
async def tickle(ctx):
    r = requests.get("https://nekos.life/api/v2/img/tickle")
    res = r.json()
    em = discord.Embed(description=f"<@{ctx.author.id}> tickles you.", colour=col)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()  
async def slap(ctx):
    r = requests.get("https://nekos.life/api/v2/img/slap")
    res = r.json()
    embed=discord.Embed(description=f"<@{ctx.author.id}> slaps you.", colour=col)
    embed.set_image(url=res['url'])
    await ctx.send(embed=embed)

@client.command()  
async def hug(ctx):
    r = requests.get("https://nekos.life/api/v2/img/hug")
    res = r.json()
    em = discord.Embed(description=f"<@{ctx.author.id}> hugs you.", colour=col)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()  
async def pat(ctx):
    r = requests.get("https://nekos.life/api/v2/img/pat")
    res = r.json()
    em = discord.Embed(description=f"<@{ctx.author.id}> pats you.", colour=col)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()   
async def kiss(ctx):
    r = requests.get("https://nekos.life/api/v2/img/kiss")
    res = r.json()
    em = discord.Embed(description=f"<@{ctx.author.id}> kisses you.", colour=col)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)
        
@client.command()
async def ping(ctx):
    await ctx.message.delete()
    before = time.monotonic()
    message = await ctx.send("Pinging...")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f":globe_with_meridians: **{int(ping)} ms**")

@client.command()
async def spamreact(ctx, count=None, reaction=None):
    await ctx.message.delete()
    if count == None or reaction == None:
        embed=discord.Embed(description=f"**Format must be {prefixstr}spamreact [count] [emoji].**", color=col)
        embed.set_footer(text=promote)
        await ctx.send(embed=embed)
    else:
        async for message in ctx.message.channel.history(limit=int(count)):
            await message.add_reaction(reaction)

@client.command()
async def masschannel(ctx):
    guild = ctx.message.guild
    await ctx.message.delete()
    count = 1
    while count < 50:
        name =  "raid"
        namea =  "raid"
        await guild.create_voice_channel(name)
        await guild.create_text_channel(namea)
        count = count + 1
    
@client.command(aliases=["shutdown", 'exit'])
async def logout(ctx):
    await ctx.message.delete()
    print(Fore.LIGHTBLUE_EX + '[/] ' + Fore.LIGHTGREEN_EX + f'Logged out: '+ Fore.LIGHTYELLOW_EX + f'Successfully logged out the self bot.' + Fore.RESET)
    await client.logout()

@client.command()
async def help(ctx, category=""):
    cat = category.lower()
    if not cat:
         await ctx.message.delete()
         embed=discord.Embed(title="__Pluto - Self Bot:__", colour=col)
         embed.add_field(name=f":stuck_out_tongue_winking_eye: Fun", value=f"`{prefixstr}help fun`", inline=True)
         embed.add_field(name=":gear: Raiding", value=f"`{prefixstr}help raid`", inline=True)
         embed.add_field(name=f":money_with_wings: Crypto", value=f"`{prefixstr}help crypto`", inline=True)
         embed.add_field(name=f":tools: Configs", value=f"`{prefixstr}help configs``", inline=True)
         embed.set_footer(text=promote)
         embed.set_thumbnail(url="https://i.pinimg.com/originals/4a/10/08/4a1008c8afc04bbc8948c7c77c4b0a50.gif")
         await ctx.send(embed=embed)
    elif cat == "crypto":
         await ctx.message.delete()
         embed = discord.Embed(
         title = '__Pluto - Self Bot (Crypto)__',
         description = f"""`{prefixstr}btc` - Displays the current bitcoin value.
         `{prefixstr}eth` - Displays the current etherium value.
         `{prefixstr}usdt` - Displays the current tether value.
         `{prefixstr}xrp` - Displays the current xrp value.
         `{prefixstr}bch` - Displays the current bitcoin cash value.
         `{prefixstr}ltc` - Displays the current litecoin value.""", color = col, inline=True)
         embed.set_footer(text=promote)
         embed.set_thumbnail(url="https://i.pinimg.com/originals/4a/10/08/4a1008c8afc04bbc8948c7c77c4b0a50.gif")
         await ctx.send(embed = embed)
    elif cat =="configs":
        await ctx.message.delete()
        embed = discord.Embed(
        title = '__Pluto - Self Bot (Configs)__',
        description = f"""`{prefixstr}prefix [newprefix]` - Allows you to change the self bots prefix.
        `{prefixstr}terminal` - Clears the bots terminal.
        `{prefixstr}afk <message>` - Sets afk message | turns on afk | turns off afk.
        `{prefixstr}playing <message>` - Status changer.
        `{prefixstr}watching <message>` - Status changer.
        `{prefixstr}streaming <message>` - Status changer.
        `{prefixstr}listening <message>` - Status changer.
        `{prefixstr}logout` - Closes the self bot.
        `{prefixstr}hypesquad [housename or random]` - Changes your hypesquad house..
        `{prefixstr}giveaway [on/off]` - Enables and disables giveaway sniper.""", color = col, inline=True)
        embed.set_footer(text=promote)
        embed.set_thumbnail(url="https://i.pinimg.com/originals/4a/10/08/4a1008c8afc04bbc8948c7c77c4b0a50.gif")
        await ctx.send(embed = embed)
    elif cat == "raid":
         await ctx.message.delete()
         embed = discord.Embed(
         title = '__Pluto - Self Bot (Raid)__',
         description = f"""`{prefixstr}raid` - Mass raids a server.
         `{prefixstr}spamreact [amount] ` - Spams reactions on messages.
         `{prefixstr}masschannel` - Spam creates new channels..
         `{prefixstr}spam [count] [message]` - Spams specified messages.
         `{prefixstr}junk` - Sends mass blank text.
         `{prefixstr}rainbowrole [role] `- Makes a role constantly change colour.
         `{prefixstr}purge [amount]` - Purges messages.
         `{prefixstr}ip` = Display ip information.""", color = col, inline=True)
         embed.set_footer(text=promote)
         embed.set_thumbnail(url="https://i.pinimg.com/originals/4a/10/08/4a1008c8afc04bbc8948c7c77c4b0a50.gif")
         await ctx.send(embed = embed)
    elif cat == "fun":
         await ctx.message.delete()
         embed = discord.Embed(
         title = '__Pluto - Self Bot (Fun)__',
         description = f"""`{prefixstr}hug <user>` - Hug a user.
         `{prefixstr}tti [text]` - Text to image.
         `{prefixstr}nitro` - Generate a random nitro code.
         `{prefixstr}snipe` - Snipes a deleted message.
         `{prefixstr}editsnipe` - Snipes a edited message.
         `{prefixstr}bigemoji` - Enlarges an emoji.
         `{prefixstr}magik` - Magikifys your pfp.
         `{prefixstr}fry` - Fryifys your pfp.
         `{prefixstr}tweet [username] [message]` - Sends a fake tweet.
         `{prefixstr}poll [question]` - Creates a poll.
         `{prefixstr}pp [user]` - Checks how big their/your pp is.
         `{prefixstr}howsimp [user]` - Checks how simp they/you are.
         `{prefixstr}howgay [user]` - Checks how gay they/you are.
         `{prefixstr}kiss <user>` - Kiss a user.
         `{prefixstr}feed <user>` - feed a user.
         `{prefixstr}slap <user>` - Slap a user.
         `{prefixstr}tickle <user>` - Tickle a user.
         `{prefixstr}pat <user>` - Pat a user.
         `{prefixstr}embed <message>` - Embeds your message.
         `{prefixstr}emojitext` - Turns your text into emojis.
         `{prefixstr}8ball <question>` - Magic 8ball.
         `{prefixstr}ping` - Checks the selfbots ping.
         `{prefixstr}firstmessage` - Finds the first message within a channel.
         `{prefixstr}minesweeper [size]` - Plays minesweeper.
         `{prefixstr}slot` - Slot machine
         `{prefixstr}wyr` - Would you rather? A or B.
         `{prefixstr}calculate [equation]` - Calculate a math equation.
         `{prefixstr}embed [message]` - Embeds a message.
         `{prefixstr}ascii [message]` - Fancy ascii text.""", color = col, inline=True)
         embed.set_footer(text=promote)
         embed.set_thumbnail(url="https://i.pinimg.com/originals/4a/10/08/4a1008c8afc04bbc8948c7c77c4b0a50.gif")
         await ctx.send(embed = embed)

with open('config.json', 'r') as f:
    d = json.load(f)
    
client.run(d["token"], bot = False) 

import discord
from discord.ext import commands
import random
import requests
import datetime

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)
client = discord.Client()



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(pass_context=True)
async def scores(ctx, date:str):
    d = [date.split('/')[0],date.split('/')[1],date.split('/')[2]]
    url = 'http://data.nba.com/5s/json/cms/noseason/scoreboard/'+d[2]+d[0]+d[1]+'/games.json'
    resp = requests.get(url=url)
    data = resp.json()
    embed = discord.Embed(title="scoreboard")
    for game in data['sports_content']['games']['game']:
        time24 = game['time']
        time = datetime.time(hour=int(time24[0:2]), minute=int(time24[2:4])).strftime('%I:%M %p')
        embed.add_field(name=game['game_url'].split('/')[1][0:3] + ' @ ' + game['game_url'].split('/')[1][3:],
                        value=game['visitor']['score'] + " - " + game['home']['score']+'\n'+time
                        )
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def addrole(ctx,*,rolerequested:str):
    member = ctx.message.author
    roles = ctx.message.server.roles
    for r in roles:
        if rolerequested == r.name:
            await bot.add_roles(member, r)
            await bot.say("added user to " + rolerequested)


@bot.command(pass_context=True)
async def removerole(ctx,*,rolerequested:str):
    member = ctx.message.author
    roles = ctx.message.server.roles
    for r in roles:
        if rolerequested == r.name:
            await bot.remove_roles(member, r)
            await bot.say("removed user from " + rolerequested)

with open('token', 'r') as myfile:
    data = myfile.read().strip()
    bot.run(data)

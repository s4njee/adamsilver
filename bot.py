import discord
from discord.ext import commands
from discord.utils import get
import random
import logging
import traceback

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

import os
import config
import discord
from discord.ext import commands

#consts
bot = commands.Bot(command_prefix = '.')
bot.remove_command('help')
root = os.path.dirname(os.path.abspath(__file__))
# bot`s comands
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(config.STATUS))
    
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        

#start bot
bot.run(config.TOKEN)
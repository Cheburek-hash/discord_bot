import discord
from discord.ext import commands
import random
import os
import requests
import config

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #bot`s events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun is ready')
    @commands.command()
    async def say(self, ctx, message):
        await ctx.send(message)
    @commands.command()
    async def bat(self, ctx):
        await ctx.send(config.BAT)
    @commands.command()
    async def spam(self, ctx, message, count = 20):
        count = int(count)
        while count > 0:
            await ctx.send(message)
            count -= 1  
    @commands.command()
    async def save(self, ctx, url):
        construct = []
        construct = url.split('.')
        typeImage = construct[-1]
        root = os.path.dirname(os.path.abspath(__file__))
        directories = ['gifs/', 'images/']
        if typeImage == 'gif':
            directory = directories[0]
        else:
            directory = directories[1]
        img = requests.get(url)
        name = str(round(random.uniform(1, 100000)))
        img_file = open(root[:-4]+ directory + name +'.'+ typeImage, 'wb')
        img_file.write(img.content)
        img_file.close()
        await ctx.send('Изображение успешно загруженно')
    @commands.command(pass_context=True)
    async def gif(self, ctx):
        responses = []
        root = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir('./gifs'):
            if filename.endswith('.gif'):
                responses.append(filename[:-4])
        directory = 'gifs/'
        randFile = root[:-4] + directory + random.choice(responses) + '.gif'
        await ctx.send(file=discord.File(randFile))
    @commands.command(pass_context=True)
    async def picture(self, ctx):
        responses = []
        root = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir('./images'):
            if filename.endswith('.jpg'):
                responses.append(filename[:-4])
        directory = 'images/'
        randFile = root[:-4] + directory + random.choice(responses) + '.jpg'
        await ctx.send(file=discord.File(randFile))
    @commands.command(pass_context=True)
    async def joke(self, ctx):
        url = "https://joke3.p.rapidapi.com/v1/joke"
        headers = {
            'x-rapidapi-host': "joke3.p.rapidapi.com",
            'x-rapidapi-key': "04c42aad27mshcf2668bb4f6ca9cp1ac772jsnaa7e45cb1396"
        }
        response = requests.request("GET", url, headers=headers)
        text = response.json()
        await ctx.send(text['content'])

def setup(bot):
    bot.add_cog(Fun(bot))
    
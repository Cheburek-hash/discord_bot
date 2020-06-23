import discord
from discord.ext import commands
import config
from discord import FFmpegPCMAudio
from discord.utils import get
import youtube_dl
import os
import random
import config

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print('Music is ready')
    @commands.command(pass_context=True)
    async def play(self, ctx, arg_1 = '/', arg_2 = '/', arg_3 = '/'):
        channel = ctx.message.author.voice.channel
        music_urls = config.MUSIC_URL
        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await self.bot.voice_clients[0].disconnect()
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        song = ''
        if arg_1 == '/':
            keys = random.sample(music_urls.keys(), len(music_urls))
            song = random.choice(keys)
            print(song)
        elif arg_2 == '/':
            song = arg_1
        elif arg_3 == '/':
            name = [arg_1, arg_2]
            song = '_'.join(name)
        else:
            name = [arg_1, arg_2, arg_3]
            song = '_'.join(name)
        
        song.title()
        for urls in music_urls:
            if song == urls:
                url = music_urls[urls]
                break
        song_there = os.path.isfile("song.wav")
        try:
            if song_there:
                os.remove("song.wav")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return

        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".wav"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.wav")
        source = FFmpegPCMAudio('song.wav')
        player = voice.play(source)

    @play.error
    async def on_error_1(self, ctx, error):
            if isinstance(error, commands.errors.CommandInvokeError):
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                player = voice.stop()
                
    @commands.command(pass_context=True, aliases=['p', 'pla'])
    async def play_url(self, ctx, url: str):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        song_there = os.path.isfile("song.wav")
        try:
            if song_there:
                os.remove("song.wav")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return

        await ctx.send("Loading..")

        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".wav"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.wav")
        source = FFmpegPCMAudio('song.wav')
        player = voice.play(source)
        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname[0]}")
        print("playing\n")
        
    @commands.command()
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        player = voice.stop()
    @commands.command(name="disconnect")
    async def disconnect(self, ctx):
        await self.bot.voice_clients[0].disconnect()
    @commands.command()
    async def music(self, ctx):
       await ctx.send(config.MUSIC)
def setup(bot):
    bot.add_cog(Music(bot))

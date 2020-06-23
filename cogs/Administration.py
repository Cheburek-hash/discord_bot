import discord
from discord.ext import commands

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #bot`s events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Administration is ready')
    
    #bot`s commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
    @commands.command()
    #@commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, ammount = 5):
        ammount = int(ammount)
        await ctx.channel.purge(limit=ammount)
    @clear.error
    async def on_error(self, ctx, error):
            if isinstance(error, commands.MissingPermissions):
                await ctx.send('У вас нет прав - вы лох')

def setup(bot):
    bot.add_cog(Administration(bot))

    
    
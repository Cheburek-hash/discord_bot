from discord.ext import commands
import config
class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print('Support is ready')
    @commands.command()
    async def help(self, ctx):
        await ctx.send(config.HELP)
def setup(bot):
    bot.add_cog(Support(bot))
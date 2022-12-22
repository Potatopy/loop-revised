import nextcord
from nextcord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music cog is ready!")

def setup(bot):
    bot.add_cog(Music(bot))
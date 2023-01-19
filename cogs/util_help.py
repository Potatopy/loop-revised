import nextcord
import os

from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()
p = os.getenv("PREFIX")

class Util_Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Util_help cog is ready!")

    @commands.group()
    async def util(self, ctx):
        pass

    @util.command()
    async def help(self, ctx: commands.Context):
        em = nextcord.Embed(title="Help", description="Help for the Util cog", color=nextcord.Color.purple())
        em.add_field(name=f"{p}afk", value="Sets you as afk", inline=False)
        em.add_field(name=f"{p}snipe", value="Snipes the last deleted message", inline=False)
        em.add_field(name=f"{p}echo", value="Echoes the message you send", inline=False)
        em.add_field(name=f"{p}poll", value="Creates a poll", inline=False)
        em.add_field(name=f"{p}ping", value="Pings the bot", inline=False)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Util_Help(bot))
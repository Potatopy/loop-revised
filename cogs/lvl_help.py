import nextcord
import os

from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()
p = os.getenv("PREFIX")

class Lvl_help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Lvl_help cog is ready!")

    @commands.group()
    async def level(self, ctx):
        pass

    @level.command()
    async def help(self, ctx):
        em = nextcord.Embed(title="Level Commands", description="Commands:", color=0x00ff00)
        em.add_field(name=f"{p}level <member>", value="Shows the level of a member.")
        em.add_field(name=f"{p}leaderboard", value="Shows the leaderboard of the server.")
        em.add_field(name=f"{p}perks", value="Shows the perks of leveling up.")
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Lvl_help(bot))
import discord
from discord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Util cog is ready!")
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def help(self, ctx):
        em = discord.Embed(description="documentation + commands: [here](https://loop-3.gitbook.io/api-docs/)", color=discord.Color.purple())
        await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(Util(bot))
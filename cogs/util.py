import discord
from discord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Util Cog has been loaded.")

    @commands.command(description="Sends the bot's ping.")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(description="Echo's a message.")
    async def echo(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(description="Loads a cog.")
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, extension):
        self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Loaded {extension}.")

    @commands.command(description="Unloads a cog.")
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Unloaded {extension}.")

    @commands.command(description="Reloads a cog.")
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, extension):
        self.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"Reloaded {extension}.")
        
def setup(bot):
    bot.add_cog(Util(bot))
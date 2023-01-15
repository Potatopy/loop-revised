import nextcord
from nextcord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot cog is ready!')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded {extension} successfully.')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded {extension} successfully.')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded {extension} successfully.')

def setup(bot):
    bot.add_cog(Owner(bot))
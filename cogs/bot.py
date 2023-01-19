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

    @commands.group()
    async def owner(self, ctx):
        pass

    @owner.command()
    async def help(self, ctx):
        embed = nextcord.Embed(title='Owner Commands', description='Commands for the bot owner.', color=nextcord.Color.blue())
        embed.add_field(name='load <ext>', value='Loads a cog.', inline=False)
        embed.add_field(name='unload <ext>', value='Unloads a cog.', inline=False)
        embed.add_field(name='reload <ext>', value='Reloads a cog.', inline=False)
        embed.set_footer(text='ONLY RUN THESE COMMANDS IF YOU KNOW WHAT YOU ARE DOING!')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Owner(bot))